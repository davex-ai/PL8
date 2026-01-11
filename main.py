from fastapi import FastAPI
from sqlalchemy import text
from db import engine, Base

app = FastAPI()

# Create tables ONCE (okay for learning, later use migrations)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Food API running"}

@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "connected"}
