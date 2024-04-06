from fastapi import APIRouter, Depends, HTTPException, Body

from ...core.auth import get_user_by_email, get_user, delete_user
from ...core.security import get_current_user, get_current_active_user
from ...db.main import get_db
from typing import List
from sqlalchemy.orm import Session

from ...db.models.user import User
from ...schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(get_db)], )


@router.get("/", response_model=List[UserRead])
async def get_all_user(
        # current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    # if not current_user:
    #     HTTPException(status_code=404)
    return db.query(User).all()


@router.get("/{_id}", response_model=UserRead)
async def get_single_user_by_id(_id: str, db: Session = Depends(get_db)):
    user = await get_user(_id=_id, db=db)
    return user


@router.delete("/{_id}", )
async def delete_user_by_id(_id, db: Session = Depends(get_db)):
    await delete_user(db, _id)
    return {"message": "user Delete", "status": 1}
