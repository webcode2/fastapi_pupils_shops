from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.main import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=True)  # For text posts
    created_at = Column(DateTime, server_default=func.now())
    media = relationship("Media", back_populates="post")  # Relationship to Media table
    author_id = Column(Integer, ForeignKey("users.id") ,unique=True)
    author=relationship("User",back_populates="posts")

class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    media_type = Column(String, nullable=False)  # "image" or "video"
    file_path = Column(String, nullable=False)  # Path to the media file
    created_at = Column(DateTime, server_default=func.now())
    post = relationship("Post", back_populates="media")
