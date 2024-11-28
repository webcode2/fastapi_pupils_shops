from sqlalchemy import Column, String,  Integer, ForeignKey ,BOOLEAN
from sqlalchemy.orm import Relationship

from app.db.main import Base
from app.db.models.mixin import Timestamp,UserBasic


class User(Timestamp, UserBasic,Base):
    __tablename__ = "users"  
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    is_activated:bool=Column(BOOLEAN, default=False)
    is_suspended:bool=Column(BOOLEAN, default=False)
    resident_info=Relationship("UserResidentInfo", back_populates="user",cascade="all, delete")
    shop=Relationship("Shop",back_populates="owner",uselist=False,cascade="all, delete")
    posts=Relationship("Post",back_populates="author",cascade="all, delete")
    user_verification_code=Relationship("VerificationCode",back_populates="user_code",cascade="all, delete")
    
    


class UserResidentInfo(Base):   
    __tablename__ = "users_resident_info"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    house_no: int = Column(Integer)
    street_name: str = Column(String(100), nullable=False)
    lga: str = Column(String(100), nullable=False)
    state_of_origin: str = Column(String(100), nullable=False)
    user = Relationship("User", back_populates="resident_info")
    user_id: int = Column(Integer, ForeignKey("users.id"))
    

class Following(Timestamp,Base):
    __tablename__="Followings"
    follower_id=int=Column(Integer,ForeignKey("users.id"),primary_key=True,nullable=False)
    following_id=int=Column(Integer,ForeignKey("users.id"),primary_key=True,nullable=False)
    
        