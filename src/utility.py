import logging
from bson import ObjectId
from typing import List
from models import UpdateSpendList
import bcrypt

def update_document(collection, spend):
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
