from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, ForeignKey, String
from sqlalchemy.sql import func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(default=0)  # Stock count
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)


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
    type: Mapped[str] = mapped_column(nullable=False)  # 'supplier' or 'customer'
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    supplier: Mapped[Supplier] = relationship(back_populates="transaction")
    customer: Mapped[Customer] = relationship(back_populates="transactions")
