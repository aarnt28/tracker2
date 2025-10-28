from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.hardware import HardwareItem


class Ticket(TimestampMixin, Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), index=True)
    hardware_item_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("hardware_items.id", ondelete="SET NULL"), index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="open", server_default=text("'open'")
    )
    priority: Mapped[str] = mapped_column(
        String(20), nullable=False, default="normal", server_default=text("'normal'")
    )
    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    client: Mapped["Client"] = relationship(back_populates="tickets")
    hardware_item: Mapped[Optional["HardwareItem"]] = relationship(back_populates="tickets")
