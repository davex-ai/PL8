from fastapi import FastAPI
from sqlalchemy import text

from database import engine, Base
import models
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)
print("API DATABASE_URL =", os.getenv("DATABASE_URL"))

@app.get("/")
def root():
    return {"status": "Food API running"}


@app.get("/db-test")
def db_test():

    try:
        with engine.connect() as conn:
            return {"result": conn.execute(text("SELECT 1")).fetchall()}
    except Exception as e:
        return {"error": str(e)}