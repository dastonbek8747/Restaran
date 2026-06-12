from fastapi import FastAPI
import uvicorn
from sqlalchemy.orm import Session
from db_connect import Base, get_db, engine
from schemas import *
from services import *
app = FastAPI()

Base.metadata.create_all(bind=engine)


# databasega kerakli jadvalni ochib yuboradi server ishga tushishi bilan

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
