from fastapi import FastAPI
from database import engine, Base
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Food API running"}


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as conn:
            return {"db": "connected"}
    except Exception as e:
        return {"error": str(e)}