import logging
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.core.token import generate_unique_code
from app.db.main import get_db
from app.db.models.user import Token
from app.schemas.tokens import PassCode, PassCodeRead

router = APIRouter(prefix="/tokens", tags=["Tokens"], dependencies=[Depends(get_db)], )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@router.get("/generate/token/",)
async def generate_token(db: Session = Depends(get_db),current_user=Depends(get_current_active_user)):
    code = generate_unique_code()
    today = datetime.today()
    exist = db.query(Token).filter(func.date(Token.created_at) == today, Token.code==code["token"]).first()
    if  exist :
        return exist

    new_code=Token(code=code["token"],created_at=datetime.now(),updated_at=datetime.now(),user_id=current_user.id)
    #
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code

@router.post("/generate/token/",)
async def generate_token(db: Session = Depends(get_db),current_user=Depends(get_current_active_user)):
    code = generate_unique_code()
    today = datetime.today()
    exist = db.query(Token).filter(func.date(Token.created_at) == today, Token.code==code["token"]).first()
    if  exist :
        return exist

    new_code=Token(code=code["token"],created_at=datetime.now(),updated_at=datetime.now(),user_id=current_user.id)
    #
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code
