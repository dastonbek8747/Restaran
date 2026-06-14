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


@app.get("/categories/{category_id}", tags=["Categories"])
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
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
            name=categorie.name,
            image_url=category.image_url

        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return {"message": "Category created"}


@app.put("/categories/{category_id}", tags=["Categories"])
async def update_category(category_id: int, category_update: ResponseCategory, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        return {"message": "Category not found"}
    else:
        category.name = category_update.name
        category.image_url = category_update.image_url
        db.commit()
        db.refresh(category)
        return {"message": "Category updated"}


@app.delete("/categories/{category_id}", tags=["Categories"])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        return {"message": "Category not found"}
    else:
        db.delete(category)
        db.commit()
        return {"message": "Category deleted"}


@app.get("/products", tags=["Products"])
async def get_all_products(db: Session = Depends(get_db)):
    return {"products": db.query(models.Product).all()}


@app.get("/products/{product_id}", tags=["Products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return {"message": "Product not found"}
    else:
        return {"product": product}


@app.post("/product", tags=["Products"])
async def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    category_product = db.query(models.Category).filter(models.Category.id == product.category_id).first()
    if not category_product:
        return {"message": "Category not found"}
    product_check = db.query(models.Product).filter(
        models.Product.name == product.name).first()
    if product_check:
        return {"message": "Product already exists"}
    else:
        new_product = models.Product(
            category=product.category_id,
            name=product.name,
            image_url=product.image_url,
            description=product.description,
            price=product.price,
            is_active=product.is_active,

        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {"message": "Product created"}


@app.put("/product/{product_id}", tags=["Products"])
async def update_product(product_id: int, product_update: UpdateProduct, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return {"message": "Product not found"}
    else:
        db_product.category = product_update.category_id
        db_product.name = product_update.name
        db_product.image_url = product_update.image_url
        db_product.description = product_update.description
        db_product.price = product_update.price
        db_product.is_active = product_update.is_active
        db.commit()
        db.refresh(db_product)
        return {"message": "Product updated"}


@app.patch("/product/{product_id}", tags=["Products"])
async def patch_product(product_id: int, product_update: PatchProduct, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return {"message": "Product not found"}
    else:
        product_data = product_update.model_dump(exclude_none=True)
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return {"message": "Product patched"}


@app.delete("/products", tags=["Products"])
async def delete_products(db: Session = Depends(get_db)):
    db.query(models.Product).delete()
    db.commit()
    return {"message": "Products deleted"}


@app.delete("/products/{product_id}", tags=["Products"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return {"message": "Product not found"}
    else:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted"}


@app.post("/login", tags=["Login/Register"])
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_login.email).first()
    if not user:
        return {"message": "User not found"}
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
