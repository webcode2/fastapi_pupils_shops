import logging
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status, Body
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from .config import Settings
from ..db.main import get_db, SessionLocal
from ..db.models.user import User
from ..schemas.tokens import Token
from ..schemas.user import UserCreate, UserLogin, UserRecoverAccount, UserRead

settings = Settings()

# Logging Functionality
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# password logics
def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def get_user(db: Session, _id, ) -> User | None:
    return db.query(User).filter(User.id == _id).first()


async def get_user_by_email(db: Session, email) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Username  and Password")
    logger.info(f"dict for user {type(user)}")
    return user


# User login jwt creation

def create_access_token(data: dict, expires_delta: timedelta = None) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="Bearer", )


# APIViewsLogic
"""
The Below functions ar called directly from route to handle task  depending on their functionalities
"""


async def authenticate_user(db: Session, email: EmailStr, password: str) -> Token:
    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    token = create_access_token(data={"id": user.id, "email": user.email, "role": user.role
                                      }, expires_delta=timedelta(days=30, minutes=30), )
    return token


async def create_user(db: Session, data: UserCreate) -> User | None:
    # logger.info(data.email)
    hashed_password = get_password_hash(data.password)
    user: User = User(
        first_name=data.first_name, phone=data.phone, last_name=data.last_name, email=data.email,
        hashed_password=hashed_password, role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def delete_user(db: Session, user_id):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, )
    db.delete(user)
    db.commit()
    return {}


async def recover_account(db: Session, account: UserRecoverAccount):
    user = await get_user_by_email(db=db, email=account.email)
    if user is None:
        raise HTTPException(status_code=404, detail={"message": "Email Not associated with any Account"})
    #     send Email Message
    return user
