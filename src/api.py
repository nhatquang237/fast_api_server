from fastapi import APIRouter

from endpoints import spends, login

api_router = APIRouter()
api_router.include_router(spends.router)
api_router.include_router(login.router)
