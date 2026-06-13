from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.orm import Session
from db_connect import Base, get_db, engine
from schemas import *
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)


# databasega kerakli jadvalni ochib yuboradi server ishga tushishi bilan

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


@app.get("/users", tags=["Users"])
async def get_all_users(db: Session = Depends(get_db)):
    return {"users": db.query(models.User).all()}


@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return {"user": db.query(models.User).filter(models.User.id == user_id).first()}


@app.post("/users", tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        password=user.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user": new_user}


@app.get("/categories", tags=["Categories"])
async def get_all_categories(db: Session = Depends(get_db)):
    return {"categories": db.query(Category).all()}


@app.get("categories/{categories_id}", tags=["Categories"])
async def category_detail(categories_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(models.Category.id == categories_id).first()
    if not category:
        return {"message": "Category not found"}
    return {"categories": category}


@app.post("/categories", tags=["Categories"])
async def create_category(categorie):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
