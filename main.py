from fastapi import FastAPI
from database import engine, Base
import models
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Food API running"}


@app.get("/db-test")
def db_test():
    print("API DATABASE_URL =", os.getenv("DATABASE_URL"))

    try:
        with engine.connect() as conn:
            return {"db": "connected"}
    except Exception as e:
        return {"error": str(e)}