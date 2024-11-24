from fastapi import APIRouter, Depends, HTTPException, Body,UploadFile,File
from ...schemas.shopSchema import PupSchema,ShopSchema
from ...controllers.auth_controller import Authenticate
from ...controllers import shop_controller
from ...core.security import get_current_user, get_current_active_user
from ...db.main import get_db
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(prefix="", tags=["market"])
pagination_page=0



@router.get("/market-place")
async def get_pups(db=Depends(get_db ) ):
    pups=await shop_controller.get_pups(db=db)   
    return pups if len(pups) >0 else HTTPException(status_code=404,detail="You're caught up for now, follow more people to see more feeds") 









@router.post("/shops")
async def create_shop(shop:ShopSchema =Body(default=None),user=Depends(get_current_user),db:Session=Depends(get_db)):
    shop= await shop_controller.create_shop(db,shop,user)
    return shop    
    



@router.get("/shops", response_model=None)
async def read_all_shops(db:Session=Depends(get_db),user=Depends(get_current_user)):
    shops=await shop_controller.read_all_shop(db=db,user=user)
    return shops

@router.get("/shops/{id}")
async def read_shop(id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    shop=await shop_controller.read_shop(db=db,user=user,id=id)
    return shop


