from fastapi import APIRouter, Depends
from app.core.security import api_key_guard

router = APIRouter()

@router.get("/", dependencies=[Depends(api_key_guard)])
async def ping():
    return {"pong": True}