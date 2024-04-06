from fastapi import APIRouter, Body, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.auth import authenticate_user, create_user, recover_account
from ...db.main import get_db
from ...schemas.tokens import Token
from ...schemas.user import UserCreate, UserLogin, UserRead, UserRecoverAccount, UserPassword

router = APIRouter(prefix="/auth",
                   tags=["Auth"],
                   responses={404: {"description": "Not found"}}, )


@router.post("/login/",response_model=Token )
async def login(body: UserLogin = Body(default=None), db: Session = Depends(get_db)):
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
