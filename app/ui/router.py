from __future__ import annotations

import asyncio
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.db.session import SessionLocal
from app.models import Client, HardwareItem, InventoryItem, Ticket

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
router = APIRouter()
MAX_ROWS = 25


def _format_temporal(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def _serialize_dashboard(session: Session) -> Dict[str, Dict[str, Any]]:
    clients_query = session.query(Client).order_by(Client.name).limit(MAX_ROWS).all()
    clients = [
        {
            "name": client.name,
            "email": client.contact_email or "",
            "phone": client.contact_phone or "",
            "notes": client.notes or "",
            "hardware_count": len(client.hardware_items),
            "ticket_count": len(client.tickets),
            "created_at": _format_temporal(client.created_at),
        }
        for client in clients_query
    ]
    clients_total = session.query(func.count(Client.id)).scalar() or 0

    hardware_query = session.query(HardwareItem).order_by(HardwareItem.name).limit(MAX_ROWS).all()
    hardware_items = [
        {
            "name": item.name,
            "serial": item.serial_number or "",
            "model": item.model_number or "",
            "status": item.status,
            "client": item.client.name if item.client else "",
            "purchase_date": _format_temporal(item.purchase_date),
            "warranty_expiration": _format_temporal(item.warranty_expiration),
        }
        for item in hardware_query
    ]
    hardware_total = session.query(func.count(HardwareItem.id)).scalar() or 0

    inventory_query = (
        session.query(InventoryItem).order_by(InventoryItem.name).limit(MAX_ROWS).all()
    )
    inventory_items = [
        {
            "sku": item.sku,
            "name": item.name,
            "quantity": item.quantity,
            "reorder_level": item.reorder_level,
            "location": item.location or "",
            "updated_at": _format_temporal(item.updated_at),
        }
        for item in inventory_query
    ]
    inventory_total = session.query(func.count(InventoryItem.id)).scalar() or 0

    tickets_query = session.query(Ticket).order_by(Ticket.opened_at.desc()).limit(MAX_ROWS).all()
    tickets = [
        {
            "title": ticket.title,
            "status": ticket.status,
            "priority": ticket.priority,
            "client": ticket.client.name if ticket.client else "",
            "hardware": ticket.hardware_item.name if ticket.hardware_item else "",
            "opened_at": _format_temporal(ticket.opened_at),
            "closed_at": _format_temporal(ticket.closed_at),
        }
        for ticket in tickets_query
    ]
    tickets_total = session.query(func.count(Ticket.id)).scalar() or 0

    return {
        "clients": {"rows": clients, "total": clients_total},
        "hardware_items": {"rows": hardware_items, "total": hardware_total},
        "inventory": {"rows": inventory_items, "total": inventory_total},
        "tickets": {"rows": tickets, "total": tickets_total},
    }


def _load_dashboard_data() -> Dict[str, Dict[str, Any]]:
    with SessionLocal() as session:
        return _serialize_dashboard(session)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    data = await asyncio.to_thread(_load_dashboard_data)
    context = {
        "request": request,
        "title": settings.APP_NAME,
        "settings": settings,
        "max_rows": MAX_ROWS,
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
        **data,
    }
    return templates.TemplateResponse("home.html", context)
