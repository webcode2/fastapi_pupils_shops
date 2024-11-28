from datetime import datetime
from typing import Optional


from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    token_type:str
    access_token:str
class UserPassword(BaseModel):
    password: str = Field(min_length=8)


class UserBase(BaseModel):
    first_name: str = Field()
    last_name: Optional[str] = Field()
    email: EmailStr
    phone: str = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "johndoe",
                "last_name": "Mike",
                "email": "johndoe@example.com",
                "phone": "08128991543"
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



# class ProfileSchema(BaseModel):
#     is_suspended: bool
#     updated_at: datetime
#     other_name: Optional[str]
#     email: str
#     id:int
#     is_activated: bool
#     created_at:datetime 
#     first_name:str
#     last_name: str
#     phone: str
#     shop: any
