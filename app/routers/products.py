from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Product
from sqlalchemy import select
from typing import List
from schemas.product import ProductRead, ProductCreate, ProductUpdate
from database import get_db

router = APIRouter(prefix="/products", tags=["Products"])


def get_product(session: Session, product_id: int) -> Product:
    """
    function to fetch a product by ID.
    Raises 404 error if product does not exist.
    """
    query = select(Product).filter(Product.id == product_id)
    result = session.execute(query).one_or_none()
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found"
        )
    return result[0]


# -------------
# FETCH all products
# -------------
@router.get("/", response_model=List[ProductRead])
def get_products(session: Session = Depends(get_db)):
    query = select(Product)
    result = session.execute(query).all()

    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
        }
        for product in result
    ]
