import math
from fastapi import APIRouter, Response, Depends, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.brand import *
from app.models import *
from app.util import *

router = APIRouter()

@router.get("/brands")
def index(page: int = 1, size: int = 10, sort ="", des: int = Query(0, alias="desc"), sc = "", so = "", sw = "", db: Session = Depends(get_db)):
    sort_direction = asc if not sort else desc if des else asc
    if not sort:
        sort = "Brand.id"
    query = (
        select(Brand.id, Brand.name)
        .select_from(Brand)
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
    brands = get_list(db, query)
    return { "brands": brands, "last": last }

@router.get("/brands/create")
def get_create(db: Session = Depends(get_db)):
    return Response()

@router.post("/brands")
async def create(payload: BrandSchema, db: Session = Depends(get_db)):
    brand = Brand(**payload.model_dump())
    db.add(brand)
    db.commit()

@router.get("/brands/{id}")
def get(id: int, db: Session = Depends(get_db)):
    query = (
        select(Brand.id, Brand.name)
        .select_from(Brand)
        .where(Brand.id == id)
    )
    brand = get_item(db, query)
    query = ( 
        select(Product.name, Product.price)
        .select_from(Brand)
        .join(Product, Brand.id == Product.brand_id)
        .where(Brand.id == id)
    )
    brandProducts = get_list(db, query)
    return { "brand": brand, "brandProducts": brandProducts }

@router.get("/brands/{id}/edit")
def edit(id: int, db: Session = Depends(get_db)):
    query = (
        select(Brand.id, Brand.name)
        .select_from(Brand)
        .where(Brand.id == id)
    )
    brand = get_item(db, query)
    query = ( 
        select(Product.name, Product.price, Product.id)
        .select_from(Brand)
        .join(Product, Brand.id == Product.brand_id)
        .where(Brand.id == id)
    )
    brandProducts = get_list(db, query)
    return { "brand": brand, "brandProducts": brandProducts }

@router.put("/brands/{id}")
async def update(id: int, payload: BrandUpdateSchema, db: Session = Depends(get_db)):
    brand = payload.model_dump()
    db.query(Brand).filter(Brand.id == id).update(brand)
    db.commit()

@router.get("/brands/{id}/delete")
def get_delete(id: int, db: Session = Depends(get_db)):
    query = (
        select(Brand.id, Brand.name)
        .select_from(Brand)
        .where(Brand.id == id)
    )
    brand = get_item(db, query)
    query = ( 
        select(Product.name, Product.price)
        .select_from(Brand)
        .join(Product, Brand.id == Product.brand_id)
        .where(Brand.id == id)
    )
    brandProducts = get_list(db, query)
    return { "brand": brand, "brandProducts": brandProducts }

@router.delete("/brands/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == id).first()
    db.delete(brand)
    db.commit()
