from fastapi import HTTPException, status
from sqlalchemy import func,or_
from sqlalchemy.orm import Session
from ..db.models.ShopModel import Pups, Shop
from ..db.models.userModel import User,Following


class Profile:
    def __init__(self, db: Session, user_id: int, ) -> None:
        self.db = db
        self.user_id = user_id

    async def all_pups(self):
        return self.db.query(Pups).filter(Pups.shop.user_id == self.user_id).all()

    async def search_pups(self, searchTerm):
        self.db.query(Pups).filter(Pups.shop.user_id == self.user_id).filter(
            func.lower(Pups.text).contains(searchTerm)).all()

    async def get_profile_details(self):
        data: Shop = await self.db.query(Shop).filter(Shop.user_id == self.user_id).first()
        return {
            "user_details": data.user.__dict__,
            "shop_details": data.__dict__
        }

    async def user_lookup(self, lookup_id):
        data = self.db.query(User).filter(User.id == lookup_id).first()
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found",
                                )
        delattr(data, "password")
        data.shop
        data.resident_info
        data.posts
        return {
            "is_owner": True if self.user_id == lookup_id else False,
            "profile": data
        }

    async def follow(self,follower_id:int,following_id:int):
        if follower_id==following_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not follow yourself")
        user_exist=self.db.query(User).filter(User.id==following_id).first()
        if user_exist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        data=Following(follower_id=follower_id,following_id=following_id)
        # TODO check for intergrity error for users trying to follow who they are already following
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return {"status_code":status.HTTP_201_CREATED,"details":"You are now following","user":following_id}
            
        
    async def unfollow(self,follower_id:int,following_id:int):
        # You can not unfollow yourself
        if follower_id==following_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not unfollow yourself")
        
        # check if user actually follows the other user as claimed
        data=self.db.query(Following).filter(follower_id=follower_id,following_id=following_id)
        
        if data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not unfollow whom you are not following")
        
        # Unfollow 
        self.db.delete(data)
        self.db.commit()
        return {"status_code":status.HTTP_201_CREATED,"details":"You have successfuly unfollowed","user":following_id}
            
        
    async def count_follow(self,user_id:int):
        data=self.db.query(Following).filter(or_ (Following.follower_id==user_id),Following.following_id==user_id).all()        
        im_following=data.flter(Following.follower_id==user_id).count()
        my_followers=data.flter(Following.following_id==user_id).count()
        return {
            "im_following":im_following,
            "my_followers":my_followers
        }
        
    

async def get_user_profile(db: Session, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    delattr(user, "password")
    user.shop
    user.posts
    user.resident_info
    return {
        "is_owner": True,
        "profile": user
    }
