from fastapi import APIRouter, Depends, Query, Header, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from db import SessionLocal
from models import Product, Category
from auth import verify_token

router = APIRouter(prefix="/products", tags=["Products"])
limiter = Limiter(key_func=get_remote_address)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


@router.get("/")
@limiter.limit("10/minute")
def get_products(
    request: Request,                 # 👈 REQUIRED FOR SLOWAPI
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    _: dict = Depends(require_token)
):
    query = db.query(Product).join(Category)

    if category:
        query = query.filter(Category.name.ilike(category))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    total = query.count()

    products = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "products": products
    }
