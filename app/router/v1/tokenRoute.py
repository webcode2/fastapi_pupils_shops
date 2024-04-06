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


@router.get("/generate/token/", response_model=PassCode)
async def generate_token(db: Session = Depends(get_db),
                         current_user=Depends(get_current_active_user),

                         ):
    code = generate_unique_code()
    today = datetime.today()

    while True:
        exist = db.query(Token).filter(func.date(Token.created_at) == today, code=code)
        if exist is not None:
            return exist

        new_code=Token(**dict(PassCodeRead(code="",created_at="",updated_at="",owner=current_user)))

        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        return new_code
