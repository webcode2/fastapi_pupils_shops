from fastapi import APIRouter, Depends, HTTPException, Body,UploadFile, File, Form
from ...schemas.shopSchema import PupSchema,ShopSchema
from ...controllers.auth_controller import Authenticate
from ...controllers import shop_controller
from ...core.security import get_current_user, get_current_active_user
from ...db.main import get_db
from typing import List
from sqlalchemy.orm import Session
from ...controllers import posts_controller  
from ...schemas.postsSchema  import PostCreate
import os
from datetime import datetime
router = APIRouter(prefix="/market-place", tags=["post"])
pagination_page=0


from fastuuid import uuid4
 

@router.post("/")
async def create_post_route(pup:str = Form(None), files: List[UploadFile] = File([]), db: Session = Depends(get_db)):
    print(pup)
    media_data = []
    for file in files:
        file.filename=f"pups_{datetime.now().strftime("%Y%m%d")}_{uuid4()}{os.path.splitext(file.filename)[1]}"
        # Save file locally or to cloud storage
        file_path =os.path.join("assets", file.filename) # Example for local storage
        with open(file_path, "wb") as f:
            f.write(await file.read())
        media_type = "image" if file.content_type.startswith("image") else "video"
        media_data.append({"media_type": media_type, "file_path": file_path})
    print(file_path)
    post_data = await PostCreate(content=pup, media=media_data)
    return posts_controller.create_post(db, post_data)


@router.get("/")
async  def read_posts(db:Session=Depends(get_db)):
    posts=await posts_controller.get_posts(db)
    return posts

@router.get("/{id}")
async  def read_post(id:int ,db:Session=Depends(get_db)):
    post=await posts_controller.get_post(db,id)
    return post

@router.patch("/{post_id}")
async def edit_post(post_id:int, db=Depends(get_db),pup:str = Form(None), files: List[UploadFile] = File([]), ):
    print(pup)
    media_data = []
    for file in files:
        file.filename=f"pups_{datetime.now().strftime("%Y%m%d")}_{uuid4()}{os.path.splitext(file.filename)[1]}"
        # Save file locally or to cloud storage
        file_path =os.path.join("assets", file.filename) # Example for local storage
        with open(file_path, "wb") as f:
            f.write(await file.read())
        media_type = "image" if file.content_type.startswith("image") else "video"
        media_data.append({"media_type": media_type, "file_path": file_path})
    post_data = PostCreate(content=pup, media=media_data)
    new_update= await posts_controller.update_post(post_id=post_id,db=db,post=post_data)

@router.delete("/{id}")
async  def read_post(id:int ,db:Session=Depends(get_db)):
    response=await posts_controller.delete_post(db,id)
    return response


