from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from advanced_alchemy.base import UUIDBase
from typing import Optional

class User(UUIDBase):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
