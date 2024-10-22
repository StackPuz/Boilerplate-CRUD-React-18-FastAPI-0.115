import bcrypt
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.config import get_db
from app.schemas.user_account import *
from app.models import *
from app.util import *

router = APIRouter()

@router.get("/profile")
def profile(request: Request, db: Session = Depends(get_db)):
    query = (
        select(UserAccount.name, UserAccount.email)
        .select_from(UserAccount)
        .where(UserAccount.id == request.state.user["id"])
    )
    userAccount = get_item(db, query)
    return { "userAccount": userAccount }

@router.post("/updateProfile")
async def update_profile(request: Request, payload: UserAccountUpdateSchema, db: Session = Depends(get_db)):
    userAccount = payload.model_dump()
    if userAccount["password"]:
        userAccount["password"] = bcrypt.hashpw(userAccount["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    else:
        del userAccount["password"]
    del userAccount["active"]
    db.query(UserAccount).filter(UserAccount.id == request.state.user["id"]).update(userAccount)
    db.commit()

@router.get("/stack")
def stack():
    return "React 18 + FastAPI 0.115 + MySQL"