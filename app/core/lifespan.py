from contextlib import asynccontextmanager
from fastapi import FastAPI
from .settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init hooks (db, redis, etc.)
    yield
    # Teardown hooks