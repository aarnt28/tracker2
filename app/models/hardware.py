from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Date, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.ticket import Ticket


class HardwareItem(TimestampMixin, Base):
    __tablename__ = "hardware_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    model_number: Mapped[Optional[str]] = mapped_column(String(128))
    serial_number: Mapped[Optional[str]] = mapped_column(String(128), unique=True)
    purchase_date: Mapped[Optional[date]] = mapped_column(Date())
    warranty_expiration: Mapped[Optional[date]] = mapped_column(Date())
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="active", server_default=text("'active'")
    )
    notes: Mapped[Optional[str]] = mapped_column(Text)

    client: Mapped[Optional["Client"]] = relationship(back_populates="hardware_items")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="hardware_item")
