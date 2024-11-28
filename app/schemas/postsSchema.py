from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MediaCreate(BaseModel):
    media_type: str  # "image" or "video"
    file_path: str


class PostCreate(BaseModel):
    content: Optional[str] = None
    media: Optional[List[MediaCreate]] = []


class Media(BaseModel):
    id: int
    media_type: str
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    content: Optional[str]
    media: List[Media] = []
    created_at: datetime

    class Config:
        orm_mode = True
