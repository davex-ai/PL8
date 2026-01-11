from db import SessionLocal
from models import Product

db = SessionLocal()

products = db.query(Product).filter(Product.original_price.is_(None)).all()

for p in products:
    p.original_price = round(p.price * 1.10, 2)

db.commit()
db.close()

print("✅ original_price updated")
