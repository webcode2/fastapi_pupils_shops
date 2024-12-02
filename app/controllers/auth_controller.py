import base64 
from urllib import parse as urlParse
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status
from jose import  jwt ,JWTError
from pydantic import EmailStr
# from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.config import Settings
from ..db.models.StaffModel import Staff
from ..schemas.user import UserCreate, UserLogin, UserRecoverAccount, UserRead,Token
from ..schemas.schemas import EmailMessage
from ..emailService import EmailService
from ..db.models.accounts_activation import VerificationCode
from  app.htmlEmails import acct_activation_code ,password_reset_request,password_reset_success,password_reset_token
from ..db.models.userModel import User

def encode_base64_url_safe(data:str):
   return urlParse.quote_from_bytes(base64.urlsafe_b64encode(data.encode("utf-8")), safe="")

def decode_base64_url_safe(data:str):
    try:
       return base64.b64decode(urlParse.unquote_to_bytes(data)).decode("utf-8")
    except:
        return "error"
     


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def create_access_token(data: dict, expires_delta: timedelta = None,reset_password:bool=False) -> str:
    to_encode = data.copy()
    
    # For email ecoding  to be sent
    if reset_password:
        to_encode.update({"exp":datetime.now()+timedelta(hours=Settings.PASSWORD_RECOVER_EMAIL_EXPIRE_HOURS)})
        return jwt.encode(to_encode,Settings.SECRET_KEY,algorithm=Settings.ALGORITHM)
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="Bearer", )


class Authenticate:
    def __init__(self, db: Session):
        self.db = db

    async def get_user(self, user_id:str,account="user") -> Staff | None:
        if account =="user":
            return self.db.query(User).filter(User.id == user_id).first()
        else:
            
            return self.db.query(Staff).filter(Staff.id == user_id).first()

    async def get_user_by_email(self, email, account: str="user") -> Staff | None:
        user=None
        if account=="user":
            user = self.db.query(User).filter(User.email == email).first()
        else:
            user = self.db.query(Staff).filter(Staff.email == email).first()
        if  user is None:
            raise HTTPException(status_code=404, detail="user doesn't exist!")
        return user

   
    async def authenticate_user(self, email: EmailStr, password: str, account: str="user") -> Token:
        user = await self.get_user_by_email(email, account=account)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password")
        if not user.is_activated:
            raise HTTPException(detail="Un-Authorized Accoutm not Verified",status_code=401)
            
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password")
        
        token = create_access_token(data={"id": user.id, "email": user.email,  "account":account                                         }, expires_delta=timedelta(days=account==30 if account=="user" else 0.5), )
        return token

    async def create_user(self, data: UserCreate, account: str="user") -> Staff|User | None:
        hashed_password = get_password_hash(data.password)
        if account == "Staff":
            user: Staff = Staff(
                first_name=data.first_name, phone=data.phone, last_name=data.last_name, email=data.email.lower(),
                password=hashed_password)          
           
            try:
                phone_exist = self.db.query(Staff).filter( Staff.phone == data.phone).first()
                email_exist=self.db.query(Staff).filter( Staff.email == data.email).first()
                if email_exist:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Staff with this Email Already Exist!")
                if phone_exist:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Staff with this Phone number Already Exist!")
                    
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"{e.__dict__}", )
            return user
        else:
            user: User = User(
                first_name=data.first_name.lower(), phone=data.phone, last_name=data.last_name.lower(), email=data.email.lower(),
            password=hashed_password)
            try:
                exist = self.db.query(User).filter(User.email == data.email).first()
                if exist:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="user with this Email Already Exist! ")
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            except IntegrityError as e:
                # TODO rewrie it to be specific
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e.__dict__}")
            mail=EmailService()
            await mail.send_message(
                EmailMessage(body="",
                             to=user.email,
                             from_email=Settings.SUPPORT_FROM_EMAIL,
                             html_body=acct_activation_code.html_content(user=user.first_name,code="3453"),
                             subject="Account Activation - Verification Code"
                             ))
           
            return user

    async def delete_user(self, user_id,account:str="user"):
        user:User|Staff|None = None
        if account=="user":            
            user = self.db.query(User).filter(User.id == user_id).first()
        else:
            user = self.db.query(Staff).filter(Staff.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, )
        self.db.delete(user)
        self.db.commit()
        return {"status":1}

    async def recover_account(self,origin:str, email: str, account: str="user",*args, **kwargs):
        user = await self.get_user_by_email(email=email, account=account)
        if user is None:
            raise HTTPException(status_code=404, detail="Email Not associated with any Account")
        #     send Email Message
        token=create_access_token(data={"_id":user.id,"_":account},reset_password=True)
        encoded=encode_base64_url_safe(data=token)        
        url=f"{origin}{encoded}"       
        print(url)
        message:EmailMessage=EmailMessage(subject="Account Recovery",to=user.email, body=url,html_body=f"<P>{url}</p>",from_email=Settings.SUPPORT_FROM_EMAIL)
        email_service=EmailService(fail_silently=True)
        await email_service.send_messages([message])
        return {"user":user,"message":"email sent"}
    
    async def change_password(self,user_id,account:str="user"):
        user=await self.get_user(user_id=user_id,account=account)     
        return {"status":1}
    
    def decode_url(token):
        visited_url=decode_base64_url_safe(token)
        jwt_token=visited_url if visited_url !="error" else ""
        try:
            data= jwt.decode(token=jwt_token,key=Settings.SECRET_KEY,algorithms=Settings.ALGORITHM)
            return data
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="forbidden")
        
        
async def activateAccountWithCode(code:int,db:Session,user_id:int):
    # VerificationCode.created_at>timedelta(datetime.now()) 
    data:VerificationCode=db.query(VerificationCode).filter(VerificationCode.code==code,VerificationCode.user_id==user_id,VerificationCode.is_used==False).first()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wrong Code or Token must have Expired")
    data.is_used=True
    data.user_code.is_activated=True
    db.commit()
    db.refresh(data)
    return {"status":status.HTTP_202_ACCEPTED,"details":"Account Activated!!!"}
    
    
        
            