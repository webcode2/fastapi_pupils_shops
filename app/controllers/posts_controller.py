from sqlalchemy.orm import Session
from ..db.models.ShopModel import Pups,Shop
from ..db.models.userModel import User
from ..schemas.shopSchema import ShopSchema
from starlette import status
from fastapi import HTTPException
from app.db.models.posts.postModel import Post, Media
from app.schemas.postsSchema import PostCreate, MediaCreate,Post as PostSchema

from typing import List

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access Denied",
        headers={"WWW-Authenticate": "Bearer"},
    )


        
    
    
    
    


async def create_post(db: Session, post: PostCreate):
    db_post = Post(content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    for media in post.media:
        db_media = Media(
            post_id=db_post.id, 
            media_type=media.media_type, 
            file_path=media.file_path
        )
        db.add(db_media)
    
    db.commit()
    return db_post

async def get_posts(db: Session):
    return db.query(Post).all()


async def get_post(db: Session,post_id:int):
    post= db.query(Post).filter(Post.id==post_id).first()
    return {"id": post.id   , "content":post.content   , "media":post.media ,   "created_at": post.created_at}


async def update_post(db:Session,post_id:int,post:PostCreate):    
    exist_post=db.query(Post).filter(Post.id==post_id).first()
    if exist_post is None:
        return HTTPException(        status_code=status.HTTP_404_NOT_FOUND,        detail="resources not Found")    
    exist_post.content=post.content    
    db.commit()
    db.refresh(exist_post)
    return  exist_post

async def delete_post(db:Session,post_id:int):    
    exist_post=db.query(Post).filter(Post.id==post_id).first()
    if exist_post is None:
        return  HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="resources not Found",
        
    )


        
    
        
    db.delete(exist_post) 
    db.commit()
    return  {"status":200,"message":"DELETED"}