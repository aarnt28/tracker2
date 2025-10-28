from fastapi import APIRouter
from app.api.v1 import ping  # module, not the function

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
