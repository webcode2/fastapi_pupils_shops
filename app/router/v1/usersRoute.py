from fastapi import APIRouter, Depends, HTTPException, Body

from ...controllers.auth_controller import Authenticate
from ...controllers.profile_controller import Profile
from ...core.security import get_current_user, get_current_active_user
from ...db.main import get_db
from typing import List
from sqlalchemy.orm import Session

from ...db.models.StaffModel import Staff
from ...schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"],dependencies=[Depends(get_current_user)])


@router.get("/profile")
async def get_all_user(user=Depends(get_current_user)):   
    return user


@router.get("/profile/{_id}")
async def get_single_user_by_id(_id: int, db: Session = Depends(get_db), ):
    # TODO change the "_id" to be current user id decoded and verified from JWT
    profile=Profile(db,user_id=_id)
    user = await profile.user_lookup(lookup_id=_id)
    return user


@router.delete("/profile/{_id}", )
async def delete_user_by_id(_id, db: Session = Depends(get_db)):
    auth = Authenticate(db)
    await auth.delete_user(user_id=_id)

    return {"message": "user Delete", "status": 1}
 