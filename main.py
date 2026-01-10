from fastapi import FastAPI

from database import engine

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Food API running"}


@app.get("/db-test") #i guess this is for definning route
def db_test():
    try:
        with engine.connect() as conn:
            return {"db": "connected"}
    except Exception as e:
        return {"error": str(e)} # what is this?