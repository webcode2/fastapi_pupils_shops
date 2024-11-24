from sqlalchemy import Column, String, BOOLEAN, Integer, ForeignKey,TEXT,JSON 
from sqlalchemy.orm import Relationship

from app.db.main import Base
from app.db.models.mixin import Timestamp,UserBasic


class User(Timestamp, UserBasic,Base):
    __tablename__ = "users"  
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resident_info=Relationship("UserResidentInfo", back_populates="user")


class UserResidentInfo(Base):   
    __tablename__ = "users_resident_info"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    house_no: int = Column(Integer)
    street_name: str = Column(String(100), nullable=False)
    lga: str = Column(String(100), nullable=False)
    state_of_origin: str = Column(String(100), nullable=False)
    user = Relationship("User", back_populates="resident_info")
    user_id: int = Column(Integer, ForeignKey("users.id"))
    
