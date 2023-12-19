from decouple import AutoConfig

config = AutoConfig()

PORT = int(config("PORT"))

# Secret key to sign JWT tokens
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(config("TOKEN_EXPIRE_MINUTES"))

# MongoDB URI
DB_URI = config("DB_URI")
