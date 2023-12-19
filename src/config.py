from decouple import AutoConfig, Csv

config = AutoConfig()

PORT = int(config("PORT"))

# Secret key to sign JWT tokens
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(config("TOKEN_EXPIRE_MINUTES"))

# MongoDB URI
MONGODB_URI = config("MONGODB_URI")
ORIGINS = config("ORIGINS", cast=Csv())
