from pymongo import MongoClient
# Replace <YOUR_MONGODB_URI> with your MongoDB URI
uri = "mongodb://localhost:27017"

class DatabaseConnection:
    _instance = None

    def __init__(self) -> None:
        self.client = MongoClient(uri)
        self.client.server_info()

    def __del__(self):
        """Safe exit: Ensure always close connection to database"""
        self.client.close()

    def __new__(cls):
        """Singleton pattern: To ensure the connection to database can be reuse"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

        return cls._instance

    @classmethod
    def delete_instance(cls):
        """Enable ability to close connection on purpose"""
        del cls._instance  # Remove the reference to the instance
        cls._instance = None
