import os
from dotenv import load_dotenv

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
PASSWORD = os.environ.get("GMAIL_PASSWORD")
GMAIL_SMTP_PORT = os.environ.get("GMAIL_SMTP_PORT")
GMAIL_SMTP_SERVER = os.environ.get("GMAIL_SMTP_SERVER")
