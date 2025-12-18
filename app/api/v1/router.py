from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, mock_data


api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(mock_data.router, prefix="/mock", tags=["mock"])


