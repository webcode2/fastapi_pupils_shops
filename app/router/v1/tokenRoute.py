import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, text, extract
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.core.token import generate_unique_code
from app.db.main import get_db
from app.db.models.user import Token
from app.schemas.tokens import PassCode, PassCodeRead, PassCodeValidate

router = APIRouter(prefix="/tokens", tags=["Tokens"], dependencies=[Depends(get_db)], )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@router.get("/generate/token/", response_model=PassCodeRead)
async def generate_token(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    today = datetime.today()
    code = generate_unique_code()
    exist = db.query(Token).filter(func.date(Token.created_at) == today, Token.code == code["token"]).first()
    if exist:
        return exist

    new_code = Token(code=code["token"], created_at=datetime.now(), updated_at=datetime.now(), user_id=current_user.id)
    #
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code


@router.post("/generate/token/", response_model=PassCodeRead)
async def validate_token(data: PassCodeValidate, db: Session = Depends(get_db),
                         current_user=Depends(get_current_active_user)):
    today = datetime.today()
    now = datetime.now()
    twelve_hours_ago = now - timedelta(hours=10)
    exist = db.query(Token).filter(Token.code == data.code).filter(Token.created_at >= twelve_hours_ago).first()
    if exist:

        return PassCodeRead(host_id=exist.owner.id, host_name=f"{exist.owner.first_name} {exist.owner.last_name}",
                            code=exist.code,
                            created_at=exist.created_at, verified=exist.verified, id=exist.id,
                            updated_at=exist.updated_at)
        logger.info(exist.owner.role)
    raise HTTPException(status_code=404, detail={"message": "Invalid Token"})
