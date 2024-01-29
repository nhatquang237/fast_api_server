from pymongo import MongoClient
from fastapi import WebSocket
from settings import MONGODB_URI

class DatabaseConnection:
    _instance = None

    def __init__(self) -> None:
        self.client = MongoClient(MONGODB_URI)
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

    @property
    def spend_database(self):
        return self.client['test']

    @property
    def spend_collection(self):
        return self.spend_database['spendData']

    @property
    def shareholder_collection(self):
        return self.spend_database['shareholderData']

    @property
    def user_collection(self):
        return self.spend_database['users']

class SocketConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        # await websocket.close(reason="Socket disconnect successfully!")
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
