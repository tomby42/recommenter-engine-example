import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, func
from sqlmodel import JSON, Field, SQLModel


class EventBase(SQLModel):
    user_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    item_id: uuid.UUID | None = Field(foreign_key="item.id", nullable=True)
    event_type: str = Field(max_length=255)
    event_value: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))


class EventCreate(EventBase):
    pass


class EventPublic(EventBase):
    id: uuid.UUID
    timestamp: datetime


class Event(EventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
