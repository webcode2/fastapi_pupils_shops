import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Annotated

from ..controllers.auth_controller import Authenticate
from ..core.config import Settings
from jose import jwt, JWTError
from ..db.main import get_db
from ..db.models.StaffModel import Staff, Role
from fastapi.security import OAuth2PasswordBearer
from socketio.exceptions import ConnectionRefusedError

from ..schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: str = Depends(oauth2_scheme),socket:bool=False):     
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return payload
    except JWTError:
        if socket:
            raise ConnectionRefusedError            
        raise credentials_exception


async def get_current_active_user(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    email: str = current_user.get("email")
    if email is None:
        raise credentials_exception    
    auth: Authenticate = Authenticate(db)
    user = await auth.get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user


async def is_admin(current_user: UserRead = Depends(get_current_user)) -> bool:
    return current_user.role == Role.superuser

