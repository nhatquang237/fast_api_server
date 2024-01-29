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
    await manager.send_personal_message(f"Welcome: Client #{client_id}", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        await manager.broadcast(f"Client #{client_id} left the chat")
        manager.disconnect(websocket)

    # while True:
    #     data = await websocket.receive_text()
    #     await manager.send_personal_message(f"You wrote: {data}", websocket)
    #     await manager.broadcast(f"Client #{client_id} says: {data}")