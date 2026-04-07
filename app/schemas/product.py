from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
    price: Decimal = Field(..., ge=0, decimal_places=2)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=255)
    price: Decimal | None = Field(None, ge=0, decimal_places=2)
    quantity: int | None = Field(None, ge=0)


class ProductRead(ProductBase):
    id: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
