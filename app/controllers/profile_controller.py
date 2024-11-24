from sqlalchemy.orm import Session
from sqlalchemy import func,or_
from ..db.models.ShopModel import Pups,Shop
from ..db.models.ShopModel import User





class Profile():
    def __init__(self,db:Session,user_id:int,) -> None:
        self.db=db
        self.user_id=user_id
    
    
    async def all_pups(self):
        return self.db.query(Pups).filter(Pups.shop.user_id==self.user_id).all()
    
    async def search_pups(self ,searchTearm):
        self.db.query(Pups).filter(Pups.shop.user_id==self.user_id).filter(func.lower(Pups.text).contains(searchTearm)).all()
        
        
    async def get_profile_details(self):
        data:Shop= await self.db.query(Shop).filter(Shop.user_id==self.user_id).first()
        return {
            "user_details":data.user.__dict__,
            "shop_details":data.__dict__
        }
        
    async def user_lookup(self,lookup_id:int):        
        data= self.db.query(User).filter(User.id==lookup_id).first()       
        
        return {
            "is_owner":True if self.user_id==lookup_id else False
            ,"user_data":data.__dict__,
            "shop_info":data.shop,  
            "resident_info":data.resident_info          
        }
        

