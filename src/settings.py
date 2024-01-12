import os
from dotenv import load_dotenv

if "MONGODB_URI" in os.environ:
    # To make sure the value of uri always up to date with .env file
    del os.environ["MONGODB_URI"]
load_dotenv()

PORT = int(os.environ.get("PORT"))

# Secret key to sign JWT tokens
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(os.environ.get("TOKEN_EXPIRE_MINUTES"))


# MongoDB URI
MONGODB_URI = os.environ.get("MONGODB_URI")

ORIGINS = [origin for origin in os.environ.get("ORIGINS").split(",") if origin]

# Email sending account
EMAIL = os.environ.get("GMAIL_EMAIL")
