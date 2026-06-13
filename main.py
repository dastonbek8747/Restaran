from fastapi import FastAPI, Depends, HTTPException
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
    return {"message": "Create new user !", "user": new_user}


@app.put("/users/{user_id}", tags=["Users"])
async def update_user(user_id: int, user_data_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    else:
        user.first_name = user_data_update.first_name
        user.last_name = user_data_update.last_name
        user.email = user_data_update.email
        user.phone_number = user_data_update.phone_number
        user.password = user_data_update.password
        db.commit()
        db.refresh(user)
        return {"message": "User update", "user": user}


@app.patch("/users/{user_id}", tags=["Users"])
async def patch_user(user_id: int, user_data_update: UserPatch, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    else:
        update_user_data = user_data_update.model_dump(exclude_none=True)
        for key, value in update_user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return {"message": "User update", "user": user}


@app.delete("/users", tags=["Users"])
async def delete_all_users(db: Session = Depends(get_db)):
    db.query(models.User).delete()
    db.commit()
    return {"message": "All users deleted"}


@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    else:
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}


@app.get("/categories", tags=["Categories"])
async def get_all_categories(db: Session = Depends(get_db)):
    return {"categories": db.query(models.Category).all()}


@app.get("categories/{categories_id}", tags=["Categories"])
async def category_detail(categories_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == categories_id).first()
    if not category:
        return {"message": "Category not found"}
    return {"categories": category}


@app.post("/categories", tags=["Categories"])
async def create_category(categorie: CretaCategory, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.name == categorie.name).first()
    if category:
        return {"message": "Category already exists"}
    else:
        new_category = models.Category(
            name=categorie.name

        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return {"message": "Category created"}


@app.post("/login", tags=["Login/Register"])
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Bunday email topilmadi ")
    if user.password != user_login.password:
        return {"message": "Parol mos kelmadi !"}
    return {"message": "Successfully logged in"}


@app.post("/register", tags=["Login/Register"])
async def register_user(user_register: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_register.email).first()
    if user:
        return {"message": "User already exists"}
    else:
        new_user = models.User(
            first_name=user_register.first_name,
            last_name=user_register.last_name,
            email=user_register.email,
            phone_number=user_register.phone_number,
            password=user_register.password
        )
        db.add(new_user)
        print(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
