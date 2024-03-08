import time
import bcrypt
import logging
import base64
import os.path
import random

from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pathlib import Path
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List
from collections import defaultdict
from functools import wraps

from models.spend import UpdateSpend, AddSpend
from settings import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES, EMAIL

def update_document(collection, spend: UpdateSpend):
    collection.update_one(
        {"_id": ObjectId(spend.id)},
        {"$set": {
            "name": spend.name,
            "value": spend.value,
            "payer": spend.payer,
            "shareholder": spend.shareholder
        }}
    )

def get_oid_str(object_id: ObjectId):
    return str(object_id)

def get_ids_from_documents(ids: List[str]) -> List[ObjectId]:
    """Get id of all documents

    Args:
        documents (UpdateSpendList): List of target document

    Returns:
        List[ObjectId]: list of ObjectId
    """

    return [ObjectId(id) for id in ids]


def logger_decorator(func):
    async def wrapper(*args, **kwargs):
        # Set up logging
        logging.basicConfig(filename='function_log.txt', level=logging.INFO)

        try:
            # Log the function call
            logging.info(f"Calling function {func.__name__} with arguments {args} and keyword arguments {kwargs}")

            # Call the original function
            result = await func(*args, **kwargs)

            # Log the return value
            logging.info(f"Function {func.__name__} returned {result}")
            print("logger_decorator called")
            return result
        except Exception as e:
            # Log exception information
            logging.error(f"Exception in function {func.__name__}: {e}")
            raise  # Re-raise the exception

    return wrapper

def hash_password(password: str) -> bytes:
    """ Function to hash a password

    Args:
        password (str): password

    Returns:
        bytes: hashed password as bytes
    """
    # Generate a salt and hash the password
    # salt = bcrypt.gensalt()
    salt = b'$2b$12$MTK3hdR0BTfOWI00frC73.'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password: str, hashed_password: bytes) -> bool:
    """Function to check a password against its hash

    Args:
        password (str): password
        hashed_password (bytes): hashed password

    Returns:
        bool: result
    """

    # Check if the provided password matches the hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Function to create a JWT token
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=2) #TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode a JWT token
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def get_random_six_digit_str() -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(6))


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def gmail_send_message(target_email):
    """
    Send confirmation email with passcode to create new account
    """
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            root_path = Path(__file__).resolve().parents[1]
            secrets_path = os.path.join(root_path, "credentials.json")

            flow = InstalledAppFlow.from_client_secrets_file(secrets_path, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Call the Gmail API
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        confirmation_code = get_random_six_digit_str()
        message.set_content(f"Your confirmation code is: {confirmation_code}")

        message["To"] = target_email
        message["From"] = EMAIL
        message["Subject"] = "Confirmation Email"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        return confirmation_code
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

def create_dummy_big_data(number_of_document: int) -> List[dict]:
    """Create dummy data for testing database query with big collection

    Args:
        number_of_document (int): number of dummy document to create

    Returns:
        List[dict]: document data in json format
    """
    members = ["Phuc", "Tai", "Thanh", "Tien", "Quang"]
    return [
        AddSpend(
            name=f"Test spend {i + 1}",
            value=random.randint(1, 9) * 1000,
            payer=random.choice(members),
            shareholder=random.sample(members, k=random.randint(1, 5))
        ).model_dump() for i in range(number_of_document)
    ]

def rate_limiter(limit_rate: int, time_frame: int):
    """ Rate limiter decorator for protected routes (with token)

    Args:
        time_frame (int): time frame (in second)
        limit_rate (int): Maximum count of access per time frame

    """
    #rate counter dictionary {token: number of request}
    access_count = defaultdict(int)
    expire_time = defaultdict(float)

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            client_ip = kwargs['request'].client.host

            # Set exprie time for from first call
            now_time = time.time()
            if not expire_time[client_ip] or now_time > expire_time[client_ip]:
                expire_time[client_ip] = now_time + time_frame
                access_count[client_ip] = 0

            access_count[client_ip] += 1
            if access_count[client_ip] > limit_rate:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

            return await func(*args, **kwargs)  # Call the function that's being decorated

        return wrapper

    return decorator