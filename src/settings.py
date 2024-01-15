import os
from dotenv import load_dotenv

env_vars = os.environ

if "IN_CONTAINER" not in env_vars and "MONGODB_URI" in env_vars:
    # In normal run (directly in IDLE VS Code) only:
    # To make sure the value of uri always up to date with .env file

    ### Note:
    # The case is value of MONGODB_URI is a link, which currently include a "=" character.
    # Somehow this character cause the mismatch between link in the first run time and the rest.
    del env_vars["MONGODB_URI"]

load_dotenv()

PORT = int(env_vars.get("PORT"))

# Secret key to sign JWT tokens
SECRET_KEY = env_vars.get("SECRET_KEY")
ALGORITHM = env_vars.get("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(env_vars.get("TOKEN_EXPIRE_MINUTES"))


# MongoDB URI
MONGODB_URI = env_vars.get("MONGODB_URI")

ORIGINS = [origin for origin in env_vars.get("ORIGINS").split(",") if origin]

# Email sending account
EMAIL = env_vars.get("GMAIL_EMAIL")
