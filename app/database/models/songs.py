from __future__ import annotations

from datetime import datetime, UTC
from typing import TYPE_CHECKING

# SQLAlchemy Common Column Types
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Float,
    Numeric,
    Text,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session_factory import Base

if TYPE_CHECKING:
    from app.database.models.posts import User


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    artist: Mapped[str] = mapped_column(nullable=False)


    user: Mapped[User] = relationship("User", back_populates="songs")


    def __repr__(self): 
        return f"Song(id={self.id}, user_id={self.user_id}, name={self.name}, artist={self.artist}"