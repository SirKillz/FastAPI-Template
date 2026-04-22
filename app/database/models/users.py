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
    from app.database.models.posts import Post
    from app.database.models.songs import Song


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    user_metadata: Mapped[dict] = mapped_column(JSON)

    # Mental model for relationship() method:
    # First arg: "What Model am I related to via Foreign Key reference? (can be a class or String)"
    # Second arg: Can be many
    # back_populates: What relationship attribute on the related model points back to me? 
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user") # Refers to the attribute name on Post
    songs: Mapped[list["Song"]] = relationship("Song", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_active={self.is_active})"