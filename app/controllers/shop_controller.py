from sqlalchemy.orm import Session
from ..db.models.ShopModel import Pups, Shop
from ..db.models.userModel import User
from ..schemas.shopSchema import ShopSchema
from starlette import status
from fastapi import HTTPException

from typing import List

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access Denied",
    headers={"WWW-Authenticate": "Bearer"},
)


async def create_shop(db: Session, shop: ShopSchema, user: User):
    # validate the shop data        
    # check if user details is associated with any shop
    # if it is then denied sprevilage as one user can not create more than one shop
    new_shop = Shop(name=shop.name, Business_reg_no=shop.Business_reg_no, house_number=shop.house_number,
                    location=shop.location, state=shop.state, street_name=shop.street_name)
    print(user)
    if db.query(Shop).filter(Shop.user_id == user["id"]).first():
        return credentials_exception
    new_shop.user_id = user["id"]
    db.add(new_shop)
    db.commit()
    db.refresh(new_shop)
    return new_shop


async def read_all_shop(db: Session, user: User):
    # TODO  paginate the responds
    shops = db.query(Shop).all()
    return shops


async def read_shop(db: Session, user: User, id: int):
    # TODO  paginate the responds
    shop = db.query(Shop).filter(Shop.id == id).first()
    return shop
