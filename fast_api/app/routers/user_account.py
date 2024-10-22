import math
import bcrypt
from fastapi import APIRouter, Request, Response, Depends, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.user_account import *
from app.models import *
from app.util import *

router = APIRouter()

@router.get("/userAccounts")
def index(page: int = 1, size: int = 10, sort ="", des: int = Query(0, alias="desc"), sc = "", so = "", sw = "", db: Session = Depends(get_db)):
    sort_direction = asc if not sort else desc if des else asc
    if not sort:
        sort = "UserAccount.id"
    query = (
        select(UserAccount.id, UserAccount.name, UserAccount.email, UserAccount.active)
        .select_from(UserAccount)
    )
    query = query.order_by(sort_direction(get_column_attr(query.column_descriptions, sort)))
    if sw:
        attr = get_column_attr(query.column_descriptions, sc)
        if not attr:
            return Response(status_code=403)
        query = query.filter(get_operator(so)(attr, sw))
    query_count = query.with_only_columns(func.count()).order_by(None)
    total = int(db.execute(query_count).scalar())
    last = math.ceil(total / size)
    query = query.offset((page - 1) * size).limit(size)
    userAccounts = get_list(db, query)
    return { "userAccounts": userAccounts, "last": last }

@router.get("/userAccounts/create")
def get_create(db: Session = Depends(get_db)):
    query = ( 
        select(Role.id, Role.name)
        .select_from(Role)
    )
    roles = get_list(db, query)
    return { "roles": roles }

@router.post("/userAccounts")
async def create(request: Request, payload: UserAccountSchema, db: Session = Depends(get_db)):
    userAccount = UserAccount(**payload.model_dump())
    userAccount.password_reset_token = str(uuid.uuid4())
    userAccount.password = bcrypt.hashpw(str(uuid.uuid4()).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    if not userAccount.active:
        userAccount.active = False
    db.add(userAccount)
    db.flush()
    roles = (await request.json())['role_id']
    for role in roles:
        userRole = UserRole(user_id = userAccount.id, role_id = role)
        db.add(userRole)
    db.commit()

@router.get("/userAccounts/{id}")
def get(id: int, db: Session = Depends(get_db)):
    query = (
        select(UserAccount.id, UserAccount.name, UserAccount.email, UserAccount.active)
        .select_from(UserAccount)
        .where(UserAccount.id == id)
    )
    userAccount = get_item(db, query)
    query = ( 
        select(Role.name.label("role_name"))
        .select_from(UserAccount)
        .join(UserRole, UserAccount.id == UserRole.user_id)
        .join(Role, UserRole.role_id == Role.id)
        .where(UserAccount.id == id)
    )
    userAccountUserRoles = get_list(db, query)
    return { "userAccount": userAccount, "userAccountUserRoles": userAccountUserRoles }

@router.get("/userAccounts/{id}/edit")
def edit(id: int, db: Session = Depends(get_db)):
    query = (
        select(UserAccount.id, UserAccount.name, UserAccount.email, UserAccount.active)
        .select_from(UserAccount)
        .where(UserAccount.id == id)
    )
    userAccount = get_item(db, query)
    query = ( 
        select(UserRole.role_id)
        .select_from(UserAccount)
        .join(UserRole, UserAccount.id == UserRole.user_id)
        .where(UserAccount.id == id)
    )
    userAccountUserRoles = get_list(db, query)
    query = ( 
        select(Role.id, Role.name)
        .select_from(Role)
    )
    roles = get_list(db, query)
    return { "userAccount": userAccount, "userAccountUserRoles": userAccountUserRoles, "roles": roles }

@router.put("/userAccounts/{id}")
async def update(id: int, request: Request, payload: UserAccountUpdateSchema, db: Session = Depends(get_db)):
    userAccount = payload.model_dump()
    if userAccount["password"]:
        userAccount["password"] = bcrypt.hashpw(userAccount["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    else:
        del userAccount["password"]
    if not userAccount["active"]:
        userAccount["active"] = False
    db.query(UserAccount).filter(UserAccount.id == id).update(userAccount)
    db.flush()
    db.query(UserRole).filter(UserRole.user_id == id).delete()
    roles = (await request.json())['role_id']
    for role in roles:
        userRole = UserRole(user_id = id, role_id = role)
        db.add(userRole)
    db.commit()

@router.get("/userAccounts/{id}/delete")
def get_delete(id: int, db: Session = Depends(get_db)):
    query = (
        select(UserAccount.id, UserAccount.name, UserAccount.email, UserAccount.active)
        .select_from(UserAccount)
        .where(UserAccount.id == id)
    )
    userAccount = get_item(db, query)
    query = ( 
        select(Role.name.label("role_name"))
        .select_from(UserAccount)
        .join(UserRole, UserAccount.id == UserRole.user_id)
        .join(Role, UserRole.role_id == Role.id)
        .where(UserAccount.id == id)
    )
    userAccountUserRoles = get_list(db, query)
    return { "userAccount": userAccount, "userAccountUserRoles": userAccountUserRoles }

@router.delete("/userAccounts/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    userAccount = db.query(UserAccount).filter(UserAccount.id == id).first()
    db.delete(userAccount)
    db.commit()
