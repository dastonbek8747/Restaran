from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from db_connect import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False, index=True)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), index=True)
    name = Column(String, nullable=False, index=True)
    image_url = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True)
    quantity = Column(Integer, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, index=True)
