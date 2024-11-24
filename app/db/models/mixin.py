from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String ,BOOLEAN
from sqlalchemy.orm import declarative_mixin,mapped_column,Mapped
from app.db.main import Base


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)




@declarative_mixin
class UserBasic:
    first_name: Mapped[str] = Column(String(100), nullable=False)
    other_name: Mapped[str] = Column(String(100), nullable=True)
    last_name: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(String(255),  nullable=False)
    phone: Mapped[str] = Column(String(10),  nullable=False)
    password: Mapped[str] = Column(String(128), nullable=False)
