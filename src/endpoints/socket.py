from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# WebSocket route
@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            print(f"Received message from client: {data}")

            # Send a response back to the client
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        websocket.close()
