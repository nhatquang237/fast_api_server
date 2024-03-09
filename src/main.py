import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import PORT, ORIGINS
from api import api_router
from data_connection import DatabaseConnection


app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register an event handler to close the database connection when the server shuts down
@app.on_event("shutdown")
def shutdown_event():
    DatabaseConnection.delete_instance()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=PORT)
