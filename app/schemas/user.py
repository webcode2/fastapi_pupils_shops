from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserPassword(BaseModel):
    password: str = Field(min_length=8)


class UserBase(BaseModel):
    first_name: str = Field()
    last_name: Optional[str] = Field()
    email: EmailStr
    phone: int = Field()
    role: int = Field()

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "johndoe",
                "last_name": "Mike",
                "email": "johndoe@example.com",
                "phone": 8128991543
            }
        }


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(UserPassword, UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field()


class UserRecoverAccount(BaseModel):
    email: EmailStr = Field()
