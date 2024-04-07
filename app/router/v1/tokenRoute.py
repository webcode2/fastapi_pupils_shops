import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, text, extract
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user, is_admin
from app.core.token import generate_unique_code
from app.db.main import get_db
from app.db.models.user import Token
from app.schemas.tokens import  PassCodeRead, PassCodeValidate

router = APIRouter(prefix="/tokens", tags=["Tokens"], dependencies=[Depends(get_db)], )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@router.get("/generate/token/", response_model=PassCodeRead)
async def generate_token(db: Session = Depends(get_db),is_admin:bool=Depends(is_admin) ,current_user=Depends(get_current_active_user)):
    today = datetime.today()
    code = generate_unique_code()
    logger.info(is_admin)
    exist = db.query(Token).filter(func.date(Token.created_at) == today, Token.code == code["token"]).first()
    if exist:
        return exist

    new_code = Token(code=code["token"], created_at=datetime.now(), updated_at=datetime.now(), user_id=current_user.id)
    #
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return PassCodeRead(host_id=new_code.owner.id, host_name=new_code.owner.get_full_name(),
                            code=new_code.code,
                            created_at=new_code.created_at, verified=new_code.verified, id=new_code.id,
                            updated_at=new_code.updated_at)


@router.post("/generate/token/", response_model=PassCodeRead)
async def varify_token(data: PassCodeValidate, db: Session = Depends(get_db),
                         current_user=Depends(get_current_active_user)):
    today = datetime.today()
    now = datetime.now()
    twelve_hours_ago = now - timedelta(hours=10)
    exist = db.query(Token).filter(Token.code == data.code).filter(Token.created_at >= twelve_hours_ago).first()
    if exist:

        return PassCodeRead(host_id=exist.owner.id, host_name=exist.owner.get_full_name(),
                            code=exist.code,
                            created_at=exist.created_at, verified=exist.verified, id=exist.id,
                            updated_at=exist.updated_at)
    raise HTTPException(status_code=404, detail={"message": "Invalid Token"})
