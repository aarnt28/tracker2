from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.hardware import HardwareItem
    from app.models.ticket import Ticket


class Client(TimestampMixin, Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(32))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    hardware_items: Mapped[List["HardwareItem"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )
    tickets: Mapped[List["Ticket"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )
