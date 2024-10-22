import math
from datetime import datetime
from fastapi import APIRouter, Request, Response, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.product import *
from app.models import *
from app.util import *

router = APIRouter()

@router.get("/products")
def index(page: int = 1, size: int = 10, sort ="", des: int = Query(0, alias="desc"), sc = "", so = "", sw = "", db: Session = Depends(get_db)):
    sort_direction = asc if not sort else desc if des else asc
    if not sort:
        sort = "Product.id"
    query = (
        select(Product.id, Product.image, Product.name, Product.price, Brand.name.label("brand_name"), UserAccount.name.label("user_account_name"))
        .select_from(Product)
        .outerjoin(Brand, Product.brand_id == Brand.id)
        .outerjoin(UserAccount, Product.create_user == UserAccount.id)
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
    products = get_list(db, query)
    return { "products": products, "last": last }

@router.get("/products/create")
def get_create(db: Session = Depends(get_db)):
    query = ( 
        select(Brand.id, Brand.name)
        .select_from(Brand)
        .order_by(Brand.name.asc())
    )
    brands = get_list(db, query)
    return { "brands": brands }

@router.post("/products")
async def create(request: Request, payload: ProductSchema = Depends(ProductSchema), db: Session = Depends(get_db), imageFile: UploadFile = File(None)):
    product = Product(**payload.model_dump())
    if imageFile:
        product.image = await get_file("products", imageFile)
    product.create_user = request.state.user["id"]
    product.create_date = datetime.now()
    db.add(product)
    db.commit()

@router.get("/products/{id}")
def get(id: int, db: Session = Depends(get_db)):
    query = (
        select(Product.id, Product.name, Product.price, Brand.name.label("brand_name"), UserAccount.name.label("user_account_name"), Product.image)
        .select_from(Product)
        .outerjoin(Brand, Product.brand_id == Brand.id)
        .outerjoin(UserAccount, Product.create_user == UserAccount.id)
        .where(Product.id == id)
    )
    product = get_item(db, query)
    return { "product": product }

@router.get("/products/{id}/edit")
def edit(id: int, db: Session = Depends(get_db)):
    query = (
        select(Product.id, Product.name, Product.price, Product.brand_id, Product.image)
        .select_from(Product)
        .where(Product.id == id)
    )
    product = get_item(db, query)
    query = ( 
        select(Brand.id, Brand.name)
        .select_from(Brand)
        .order_by(Brand.name.asc())
    )
    brands = get_list(db, query)
    return { "product": product, "brands": brands }

@router.put("/products/{id}")
async def update(id: int, payload: ProductUpdateSchema = Depends(ProductUpdateSchema), db: Session = Depends(get_db), imageFile: UploadFile = File(None)):
    product = payload.model_dump()
    if imageFile:
        product["image"] = await get_file("products", imageFile)
    db.query(Product).filter(Product.id == id).update(product)
    db.commit()

@router.get("/products/{id}/delete")
def get_delete(id: int, db: Session = Depends(get_db)):
    query = (
        select(Product.id, Product.name, Product.price, Brand.name.label("brand_name"), UserAccount.name.label("user_account_name"), Product.image)
        .select_from(Product)
        .outerjoin(Brand, Product.brand_id == Brand.id)
        .outerjoin(UserAccount, Product.create_user == UserAccount.id)
        .where(Product.id == id)
    )
    product = get_item(db, query)
    return { "product": product }

@router.delete("/products/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    db.delete(product)
    db.commit()
