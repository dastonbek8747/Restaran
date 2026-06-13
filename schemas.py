from pydantic import BaseModel, Field, EmailStr, model_validator


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


class UserDelete(BaseModel):
    id: int
    email: EmailStr


class UserUpdate(UserCreate):
    pass


class Category(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    category_id: int
    name: str
    image_url: str
    description: str
    price: float
    quantity: int
    is_active: bool
