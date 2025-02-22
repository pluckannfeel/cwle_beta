from fastapi import APIRouter
from app.api.v1.endpoints import health_check, chat, user

api_router = APIRouter()

api_router.include_router(
    health_check.router, prefix="/health", tags=["health"])
# api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
