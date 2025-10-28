from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


# Import models so Alembic registers the mapped tables.
from app import models  # noqa: E402,F401
