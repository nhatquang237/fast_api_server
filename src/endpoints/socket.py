from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer

from data_connection import SocketConnectionManager

router = APIRouter()
manager = SocketConnectionManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# WebSocket route
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(websocket, data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
