# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    num_reviews = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")
