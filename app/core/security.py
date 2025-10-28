from fastapi import Header, HTTPException, status
from passlib.context import CryptContext
from .settings import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def api_key_guard(x_api_key: str | None = Header(default=None)):
    if not x_api_key or x_api_key != settings.API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

async def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd.verify(plain, hashed)
    except Exception:
        return False