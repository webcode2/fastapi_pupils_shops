import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Annotated

from .auth import get_user, get_user_by_email
from ..core.config import Settings
from jose import jwt, JWTError
from ..db.main import get_db
from ..db.models.user import User, Role
from fastapi.security import OAuth2PasswordBearer

from ..schemas.tokens import TokenData
from ..schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")
settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        logger.info(token)
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserRead = Depends( get_current_user)):

    # if current_user.id == 1:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    # logger.info( dict(await current_user))
    return current_user


async def  is_admin(current_user:UserRead=Depends(get_current_user))->bool:
    return current_user.role==Role.superuser
