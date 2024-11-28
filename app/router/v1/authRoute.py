import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...controllers.auth_controller import Authenticate,activateAccountWithCode
from ...core.security import get_current_active_user
from ...db.main import get_db
from ...schemas.user import UserCreate, UserLogin, UserRead, UserPassword,Token

router = APIRouter(prefix="/auth",
                   tags=["Auth"],
                   responses={404: {"description": "Not found"}} )


@router.post("/token/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    auth: Authenticate = Authenticate(db=db)
    token = await auth.authenticate_user(email=form_data.username, password=form_data.password, account="Staff")
    return token


@router.post("/login/", response_model=Token)
async def login(body: UserLogin, db: Session = Depends(get_db)):
    auth: Authenticate = Authenticate(db=db)

    token = await auth.authenticate_user(email=body.email, password=body.password)
    return token


@router.post("/register/", response_model=UserRead)
async def register(user: UserCreate = Body(default=None), db: Session = Depends(get_db)):
    auth: Authenticate = Authenticate(db=db)
    new_user = await auth.create_user(data=user)
    return new_user


# password recovery logics
@router.post("/recover-password/", )
async def initiate_password_recovery(request:Request ,email: str, db: Session = Depends(get_db),    ):
    auth: Authenticate = Authenticate(db=db)
    return await auth.recover_account( origin=request.url, email=email)


@router.post("/recover-account/{token}/")
async def reset_password(token,  password: UserPassword = Body(default=None)):
    return {"email": token,  **dict(password)}


@router.post("/change_password")
async def change_password(old_password:UserPassword=Body(default=None),db:Session=Depends(get_db),current_user:UserRead=Depends(get_current_active_user)):
    auth:Authenticate=Authenticate(db=db)
    auth.change_password(user_id=current_user.id)
    
    
    
@router.post("/activate")
async def acctivate_account(user=Body(default=None),db:Session=Depends(get_db)):
    data= await activateAccountWithCode(code=user["code"],db=db,user_id=user["user_id"])
    # return data
    return (data)