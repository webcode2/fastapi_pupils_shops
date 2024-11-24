from sqlalchemy import Column, String, BOOLEAN, Integer, ForeignKey,TEXT,JSON 
from sqlalchemy.orm import Relationship

from app.db.main import Base
from app.db.models.mixin import Timestamp
from app.db.models.userModel import User
from app.db.models.ShopModel import Shop



class userActivate(Timestamp, Base):
    __tablename__ = "users_acccount_status"  
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status:bool=Column(BOOLEAN, default=False)
    
    user_id:int=Column(Integer,ForeignKey("users.id"),unique=True)
    user=Relationship("User",back_populates="status",uselist=False)
    

class ShopActivate(Timestamp, Base):
    __tablename__ = "shop_acccount_status"  
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    is_activated:bool=Column(BOOLEAN, default=False)
    is_active: bool = Column(BOOLEAN, default=True)
    is_suspended: bool = Column(BOOLEAN, default=False)         
    
    shop_id:int=Column(Integer,ForeignKey("shops.id"),unique=True)
    shop=Relationship("Shop",back_populates="status     ",uselist=False)



class VerificationCode(Timestamp,Base):
    __tablename__="verification_code"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code:int=Column(Integer,index=True)
    
    user_id:int=Column(Integer,ForeignKey("users.id"),unique=True)
    user=Relationship("User",back_populates="status",uselist=False)
    
    is_used:bool=  Column(BOOLEAN, default=False)

        