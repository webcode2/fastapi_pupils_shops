from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

# JWT Token Functionality
from app.db.models.user import User


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "access_token": "3333333-3-k",
                "token_type": "Bearer",

            }
        }


class TokenData(BaseModel):
    id:int
    role:int
    email: str


#
#
"""
THE ABOVE CODE IS JUST FOR JWT MODELS 
"""


class PassCode(BaseModel):
    code: str
    # owner: User
    created_at: datetime
    updated_at: datetime


class PassCodeRead(PassCode):
    id: int
    verified: bool

