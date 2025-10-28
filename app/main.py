from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.settings import settings
from app.core.logging import setup_logging
from app.core.lifespan import lifespan
from app.api.v1.router import api_router

setup_logging()
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Trusted hosts (Zoraxy will forward the original host)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS + ["*"] if settings.APP_ENV == "dev" else settings.ALLOWED_HOSTS)

# CORS for iPad/Shortcuts and web
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
async def health(request: Request):
    return {"ok": True, "client": request.client.host}

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def _metrics():
    Instrumentator().instrument(app).expose(app)