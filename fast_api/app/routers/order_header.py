import math
from fastapi import APIRouter, Response, Depends, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.order_header import *
from app.models import *
from app.util import *

router = APIRouter()

@router.get("/orderHeaders")
def index(page: int = 1, size: int = 10, sort ="", des: int = Query(0, alias="desc"), sc = "", so = "", sw = "", db: Session = Depends(get_db)):
    sort_direction = asc if not sort else desc if des else asc
    if not sort:
        sort = "OrderHeader.id"
    query = (
        select(OrderHeader.id, Customer.name.label("customer_name"), OrderHeader.order_date)
        .select_from(OrderHeader)
        .outerjoin(Customer, OrderHeader.customer_id == Customer.id)
    )
    query = query.order_by(sort_direction(get_column_attr(query.column_descriptions, sort)))
    if sw:
        attr = get_column_attr(query.column_descriptions, sc)
        if not attr:
            return Response(status_code=403)
        if (sc == 'OrderHeader.order_date'):
            sw = get_date_query(sw)
        query = query.filter(get_operator(so)(attr, sw))
    query_count = query.with_only_columns(func.count()).order_by(None)
    total = int(db.execute(query_count).scalar())
    last = math.ceil(total / size)
    query = query.offset((page - 1) * size).limit(size)
    orderHeaders = get_list(db, query)
    return { "orderHeaders": orderHeaders, "last": last }

@router.get("/orderHeaders/create")
def get_create(db: Session = Depends(get_db)):
    query = ( 
        select(Customer.id, Customer.name)
        .select_from(Customer)
        .order_by(Customer.name.asc())
    )
    customers = get_list(db, query)
    return { "customers": customers }

@router.post("/orderHeaders")
async def create(payload: OrderHeaderSchema, db: Session = Depends(get_db)):
    orderHeader = OrderHeader(**payload.model_dump())
    db.add(orderHeader)
    db.commit()

@router.get("/orderHeaders/{id}")
def get(id: int, db: Session = Depends(get_db)):
    query = (
        select(OrderHeader.id, Customer.name.label("customer_name"), OrderHeader.order_date)
        .select_from(OrderHeader)
        .outerjoin(Customer, OrderHeader.customer_id == Customer.id)
        .where(OrderHeader.id == id)
    )
    orderHeader = get_item(db, query)
    query = ( 
        select(OrderDetail.no, Product.name.label("product_name"), OrderDetail.qty)
        .select_from(OrderHeader)
        .join(OrderDetail, OrderHeader.id == OrderDetail.order_id)
        .join(Product, OrderDetail.product_id == Product.id)
        .where(OrderHeader.id == id)
    )
    orderHeaderOrderDetails = get_list(db, query)
    return { "orderHeader": orderHeader, "orderHeaderOrderDetails": orderHeaderOrderDetails }

@router.get("/orderHeaders/{id}/edit")
def edit(id: int, db: Session = Depends(get_db)):
    query = (
        select(OrderHeader.id, OrderHeader.customer_id, OrderHeader.order_date)
        .select_from(OrderHeader)
        .where(OrderHeader.id == id)
    )
    orderHeader = get_item(db, query)
    query = ( 
        select(OrderDetail.no, Product.name.label("product_name"), OrderDetail.qty, OrderDetail.order_id)
        .select_from(OrderHeader)
        .join(OrderDetail, OrderHeader.id == OrderDetail.order_id)
        .join(Product, OrderDetail.product_id == Product.id)
        .where(OrderHeader.id == id)
    )
    orderHeaderOrderDetails = get_list(db, query)
    query = ( 
        select(Customer.id, Customer.name)
        .select_from(Customer)
        .order_by(Customer.name.asc())
    )
    customers = get_list(db, query)
    return { "orderHeader": orderHeader, "orderHeaderOrderDetails": orderHeaderOrderDetails, "customers": customers }

@router.put("/orderHeaders/{id}")
async def update(id: int, payload: OrderHeaderUpdateSchema, db: Session = Depends(get_db)):
    orderHeader = payload.model_dump()
    db.query(OrderHeader).filter(OrderHeader.id == id).update(orderHeader)
    db.commit()

@router.get("/orderHeaders/{id}/delete")
def get_delete(id: int, db: Session = Depends(get_db)):
    query = (
        select(OrderHeader.id, Customer.name.label("customer_name"), OrderHeader.order_date)
        .select_from(OrderHeader)
        .outerjoin(Customer, OrderHeader.customer_id == Customer.id)
        .where(OrderHeader.id == id)
    )
    orderHeader = get_item(db, query)
    query = ( 
        select(OrderDetail.no, Product.name.label("product_name"), OrderDetail.qty)
        .select_from(OrderHeader)
        .join(OrderDetail, OrderHeader.id == OrderDetail.order_id)
        .join(Product, OrderDetail.product_id == Product.id)
        .where(OrderHeader.id == id)
    )
    orderHeaderOrderDetails = get_list(db, query)
    return { "orderHeader": orderHeader, "orderHeaderOrderDetails": orderHeaderOrderDetails }

@router.delete("/orderHeaders/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    orderHeader = db.query(OrderHeader).filter(OrderHeader.id == id).first()
    db.delete(orderHeader)
    db.commit()
