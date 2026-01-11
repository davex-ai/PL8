from fastapi import FastAPI
from sqlalchemy import text

from db import engine, Base
import os
import db

app = FastAPI()

Base.metadata.create_all(bind=engine)
print("API DATABASE_URL =", os.getenv("DATABASE_URL"))
print("DATABASE MODULE FILE =", db.__file__)
print("ENGINE URL =", engine.url)

@app.get("/")
def root():
    return {"status": "Food API running"}


@app.get("/db-test")
def db_test():
    print("ENGINE URL INSIDE ROUTE =", engine.url)

    try:
        with engine.connect() as conn:
            return {"result": conn.execute(text("SELECT 1")).fetchall()}
    except Exception as e:
        return {"error": str(e)}