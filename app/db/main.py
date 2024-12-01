from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Replace "your_database.db" with your desired database filename
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:771531@localhost:5432/puppies"

if bool(os.getenv("ENVIRONMENT",default="0"))==True:
    engine = create_engine(os.getenv("LOCAL_DATABASE_CONNECTION_STRING",default="postgresql://postgres:771531@localhost:5432/puppies"))
    print("local Env")
else:
    engine = create_engine(os.getenv("DATABASE_CONNECTION_STRING",default=""))
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
