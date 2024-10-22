import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config import get_db, config
from app.models import *
from app.util import send_mail

router = APIRouter()

def get_user_roles(user_id: int):
    with next(get_db()) as db:
        roles = db.query(Role.name).join(UserRole, Role.id == UserRole.role_id).filter(UserRole.user_id == user_id).all()
        return [role[0] for role in roles]

def get_menu(roles: list):
    return [
        { "title": item["title"], "path": item["path"] }
        for item in config["menu"] if item["show"] and (not item.get("roles") or any(role in item["roles"].split(",") for role in roles))
    ]

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    user = db.query(UserAccount).filter(UserAccount.name == payload["name"]).first()
    if user and user.active and bcrypt.checkpw(payload["password"].encode('utf-8'), user.password.encode('utf-8')):
        roles = get_user_roles(user.id)
        exp = datetime.utcnow() + timedelta(days=1)
        token = jwt.encode({ "id": user.id, "name": user.name, "roles": roles, "exp": exp }, config["jwtSecret"])
        return { "token": token, "user": { "name": user.name, "menu": get_menu(roles) } }
    message = "User is disabled" if user and not user.active else "Invalid credentials"
    return JSONResponse({ "message": message }, 400)

@router.get("/user")
def get_user(request: Request):
    return { "name": "admin", "menu": get_menu(get_user_roles(request.state.user["id"])) }

@router.get("/logout")
def logout():
    return

@router.post("/resetPassword")
async def reset_password(request: Request, db: Session = Depends(get_db)):
    email = (await request.json())["email"]
    user = db.query(UserAccount).filter(UserAccount.email == email).first()
    if user:
        token = str(uuid.uuid4())
        user.password_reset_token = token
        db.commit()
        send_mail("reset", email, token)
        return
    return Response(status_code=404)

@router.get("/changePassword/{token}")
def get_change_password(token: str, db: Session = Depends(get_db)):
    user = db.query(UserAccount).filter(UserAccount.password_reset_token == token).first()
    if user:
        return
    return Response(status_code=404)

@router.post("/changePassword/{token}")
async def change_password(request: Request, token: str, db: Session = Depends(get_db)):
    user = db.query(UserAccount).filter(UserAccount.password_reset_token == token).first()
    if user:
        password = (await request.json())["password"]
        user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password_reset_token = None
        db.commit()
        return
    return Response(status_code=404)