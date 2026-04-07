from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    Float,
    ForeignKey,
    String,
    Enum,
    NUMERIC,
    CheckConstraint,
)
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base


# ----------------------
# ENUMS
# ----------------------
class TransactionType(Enum):
    supplier = "supplier"
    customer = "customer"


# ----------------------
# PRODUCT
# ----------------------
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)  # Stock count
    price: Mapped[float] = mapped_column(NUMERIC(10, 2), nullable=False, default=0.0)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = CheckConstraint(
        "quantity >= 0", name="check_product_quantity_non_negative"
    )


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    contact: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="supplier")


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    contact: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0)
    address: Mapped[str] = mapped_column(String(100), nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="customer")


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[str] = mapped_column(Enum(TransactionType), nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    supplier: Mapped[Supplier] = relationship(back_populates="transactions")
    customer: Mapped[Customer] = relationship(back_populates="transactions")
