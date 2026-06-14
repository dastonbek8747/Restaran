from pydantic import BaseModel, Field, EmailStr, model_validator
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=5)
    phone_number: str = Field(min_length=9, max_length=13)
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Parollar mos kelmadi")
        return self


class UserResponse(BaseModel):
    id: int
    first_name: str
    phone_number: int
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    password: str


class UserPatch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CretaCategory(BaseModel):
    name: str
    image_url:str


class ResponseCategory(BaseModel):
    id: int
    name: str
    image_url: str


class CreateProduct(BaseModel):
    category_id: int
    name: str
    image_url: str
    description: str
    price: int
    is_active: bool


class UpdateProduct(CreateProduct):
    pass


class PatchProduct(BaseModel):
    category_id: int
    product_id: int
    name: str | None = None
    image_url: str | None = None
    description: str | None = None
    price: int | None = None
    is_active: bool | None = None


class DeleteProduct(BaseModel):
    id: int


class OrderCreate(BaseModel):
    user_id: int
    total_price: int
    status: str
    created_at: datetime


class PatchOrder(BaseModel):
    user_id: int
    total_price: int | None = None
    status: str | None = None
    created_at: datetime | None = None


class ResponseOrder(BaseModel):
    id: int
    user_id: int
    total_price: int
    status: str
    created_at: datetime


class CreateOrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: int


class UpdateOrderItem(CreateOrderItem):
    pass

class PatchOrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: int
