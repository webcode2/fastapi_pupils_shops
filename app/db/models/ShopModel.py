from sqlalchemy import Column, String, BOOLEAN, Integer, ForeignKey,TEXT,JSON 
from sqlalchemy.orm import Relationship

from app.db.main import Base
from app.db.models.mixin import Timestamp,UserBasic
from app.db.models.userModel import User, UserResidentInfo




class Shop(Timestamp, Base):
    __tablename__ = "shops"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(100), nullable=False)
    location: str = Column(String(100), nullable=False)
    state: str = Column(String(255), nullable=False)
    street_name: str = Column(String(255), nullable=False)
    house_number: str = Column(String(10), nullable=False)
    Business_reg_no: str = Column(String(128), nullable=True,)
   
    
    user = Relationship("User", uselist=False)
    user_id = Column(Integer, ForeignKey("users.id") ,unique=True)
    
    pups=Relationship("Pups",back_populates="shop")
    
    
 
class Pups(Timestamp ,Base):
    __tablename__="pups"
    id:int=Column(Integer,primary_key=True,autoincrement=True)
    text:str=Column(TEXT ,nullable=True)
    img_urls:str=Column(JSON)
    
    shop_id:int=Column(Integer,ForeignKey("shops.id"))
    shop=Relationship("Shop",back_populates="pups",uselist=False)
    breed_id:int=Column(Integer,ForeignKey("breeds.id"))
    breed=Relationship("Breed",uselist=False, back_populates="pups")
    categories=Relationship("Category",secondary="pups_category")
    
    
class Breed(Base):
    __tablename__="breeds"
    id:int =Column(Integer ,primary_key=True, index=True, autoincrement=True)
    name:str=Column(String(255), unique=True, nullable=False)
    pups=Relationship("Pups",back_populates="breed")
    
    
class Category(Base):
    __tablename__="categories"
    id:str=Column(Integer, autoincrement=True, primary_key=True,nullable=False)
    name:str=Column(String(255),unique=True,nullable=False)
    
    
    
    
class PupsCategory(Base):
    __tablename__="pups_category"
    pups_id=Column(Integer,ForeignKey("pups.id"),primary_key=True)
    category_id=Column(Integer,ForeignKey("categories.id"),primary_key=True)
    
   
class PupsBreed(Base):
    __tablename__="pups_breed"
    pups_id=Column(Integer,ForeignKey("pups.id"),primary_key=True)
    breed_id=Column(Integer,ForeignKey("breeds.id"),primary_key=True)
    
   