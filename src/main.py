import uvicorn

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from settings import PORT, ORIGINS
from api import api_router

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket route
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        # Receive message from the client
        data = await websocket.receive_text()
        print(f"Received message from client: {data}")

        # Send a response back to the client
        await websocket.send_text(f"Message received: {data}")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=PORT)

"""
Finish email confirmation feature
"""
