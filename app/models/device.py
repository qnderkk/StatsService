import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.database import Base

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(
        back_populates="devices"
    )
    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan"
    )