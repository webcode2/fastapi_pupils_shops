import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.auth import authenticate_user, create_user, recover_account
from ...db.main import get_db
from ...schemas.tokens import Token
from ...schemas.user import UserCreate, UserLogin, UserRead, UserRecoverAccount, UserPassword

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

router = APIRouter(prefix="/auth",
                   tags=["Auth"],
                   responses={404: {"description": "Not found"}}, )



@router.post("/token/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)):
    logger.info(form_data.username)
    logger.info(form_data.password)
    token = await authenticate_user(db=db, email=form_data.username, password=form_data.password)
    return token







@router.post("/login/",response_model=Token )
async def login(body :UserLogin , db: Session = Depends(get_db)):
    token = await authenticate_user(db=db, email=body.email, password=body.password)
    return token


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate = Body(default=None), db: Session = Depends(get_db)):
    new_user = await create_user(db=db, data=user)
    return new_user


# password recovery logics

@router.post("/recover-password/", )
async def initiate_password_recovery(email: UserRecoverAccount = Body(default=None), db: Session = Depends(get_db)):
    return await recover_account(db=db, account=email)


@router.post("/recover-account/{email}/{last_login}")
async def reset_password(email, last_login, password: UserPassword = Body(default=None)):
    return {"email": email, "last_login": last_login, **dict(password)}
