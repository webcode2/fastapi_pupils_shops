import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...controllers.auth_controller import Authenticate
from ...core.security import get_current_active_user
from ...db.main import get_db
from ...schemas.user import UserCreate, UserLogin, UserRead, UserPassword,Token

router = APIRouter(prefix="/accounts/staff/auth",
                   tags=["Admin_Auth_route"],
                   responses={404: {"description": "Not found"}}, )


@router.post("/token/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    auth: Authenticate = Authenticate(db=db)
    token = await auth.authenticate_user(email=form_data.username, password=form_data.password, account="Staff")
    return token


@router.post("/login/", response_model=Token)
async def login(body: UserLogin, db: Session = Depends(get_db)):
    auth: Authenticate = Authenticate(db=db)
    token = await auth.authenticate_user(email=body.email, password=body.password, account="Staff")
    return token


@router.post("/register/", response_model=UserRead)
async def register(user: UserCreate = Body(default=None), db: Session = Depends(get_db)):
    auth: Authenticate = Authenticate(db=db)

    new_user = await auth.create_user(data=user, account="Staff")
    if hasattr(new_user,"id"):
        #TODO Send email to the user email address
        pass
    return new_user


# password recovery logics

@router.post("/recover-password/", )
async def initiate_password_recovery(request:Request,email: str=Body(default=None), db: Session = Depends(get_db),    ):
    auth: Authenticate = Authenticate(db=db)
    return await auth.recover_account( origin=request.url,account="staff", email=email)


@router.post("/recover-password/{token}")
async def reset_password(token,  password: UserPassword = Body(default=None)):
   user:dict= Authenticate.decode_url(token)
   if user.get("_id") and user.get("_") is not None:
    #    TODO
    #    Get the user and change the password
    #    upon successful password change, Send an email to the user (password changed successful)
    #    Return status code of 201 with a detail of 1 for true
       pass     
   return {"email": token,"id":user["_id"],"account":user["_"],  **dict(password)}


@router.get("/recover-password/{token}")
async def reset_password(token):    
    return Authenticate.decode_url(token)

@router.post("/change_password")
async def change_password(old_password:UserPassword=Body(default=None),db:Session=Depends(get_db),current_user:UserRead=Depends(get_current_active_user)):
    auth:Authenticate=Authenticate(db=db)
    auth.change_password(user_id=current_user.id)
    
    