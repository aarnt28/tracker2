from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.settings import settings

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "title": settings.APP_NAME,
        "settings": settings,
        "endpoints": [
            {"label": "Health Check", "path": "/health", "description": "Application heartbeat"},
            {
                "label": "Metrics",
                "path": "/metrics",
                "description": "Prometheus metrics (starts after first request)",
            },
            {
                "label": "API v1 Ping",
                "path": "/api/v1/ping/",
                "description": "Authenticated ping endpoint (requires X-API-Key header)",
            },
            {"label": "API Docs", "path": "/docs", "description": "Interactive Swagger UI"},
        ],
    }
    return templates.TemplateResponse("home.html", context)
