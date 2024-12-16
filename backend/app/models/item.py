import uuid
from datetime import datetime
from typing import Sequence

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel
from .user import User


# Shared properties
class ItemBase(SQLModel):
    name: str | None = Field(min_length=1, max_length=255)
    year: int | None = Field(nullable=True)
    selling_price: float | None = Field(default=None)
    km_driven: float | None = Field(default=None)
    fuel_type: str | None = Field(default=None, max_length=255)
    transmission: str | None = Field(default=None, max_length=255)
    owner_type: str | None = Field(default=None, max_length=255)
    mileage: float | None = Field(default=None)
    engine: str | None = Field(default=None, max_length=255)
    max_power: float | None = Field(default=None)
    torque: str | None = Field(default=None, max_length=255)
    seats: int | None = Field(default=None)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: uuid.UUID
    seller_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    seller_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    sold_at: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    final_price: float | None = Field(default=None)


class ItemsPublic(SQLModel):
    data: Sequence[Item]
    count: int


class ItemQuery(SQLModel):
    min_year: int | None
    min_price: float | None
    max_price: float | None
    max_km_driven: float | None
    fuel_type: str | None


class UserItemRecommendQuery(SQLModel):
    query: ItemQuery | None
    item_id: uuid.UUID | None
