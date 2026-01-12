from fastapi import FastAPI
from sqlalchemy import text
from starlette.staticfiles import StaticFiles

from db import engine, Base
from routers.product import router as products_router
from auth import create_access_token
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register product router
app.include_router(products_router)

# Create tables (once)
Base.metadata.create_all(bind=engine)

# Root
@app.get("/")
def root():
    return {"status": "Food API running"}

# Dev token route (must be outside router)
@app.get("/dev-token")
def dev_token():
    return {"access_token": create_access_token({"scope": "read"})}

# DB test
@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "connected"}

# Rate limit handler
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )
