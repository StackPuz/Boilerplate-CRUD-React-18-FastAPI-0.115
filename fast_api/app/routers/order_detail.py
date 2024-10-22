import math
from fastapi import APIRouter, Response, Depends, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.order_detail import *
from app.models import *
from app.util import *

router = APIRouter()

@router.get("/orderDetails/create")
def get_create(db: Session = Depends(get_db)):
    query = ( 
        select(Product.id, Product.name)
        .select_from(Product)
        .order_by(Product.name.asc())
    )
    products = get_list(db, query)
    return { "products": products }

@router.post("/orderDetails")
async def create(payload: OrderDetailSchema, db: Session = Depends(get_db)):
    orderDetail = OrderDetail(**payload.model_dump())
    db.add(orderDetail)
    db.commit()

@router.get("/orderDetails/{order_id}/{no}/edit")
def edit(order_id: int, no: int, db: Session = Depends(get_db)):
    query = (
        select(OrderDetail.order_id, OrderDetail.no, OrderDetail.product_id, OrderDetail.qty)
        .select_from(OrderDetail)
        .where(OrderDetail.order_id == order_id)
        .where(OrderDetail.no == no)
    )
    orderDetail = get_item(db, query)
    query = ( 
        select(Product.id, Product.name)
        .select_from(Product)
        .order_by(Product.name.asc())
    )
    products = get_list(db, query)
    return { "orderDetail": orderDetail, "products": products }

@router.put("/orderDetails/{order_id}/{no}")
async def update(order_id: int, no: int, payload: OrderDetailUpdateSchema, db: Session = Depends(get_db)):
    orderDetail = payload.model_dump()
    db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.no == no).update(orderDetail)
    db.commit()

@router.get("/orderDetails/{order_id}/{no}/delete")
def get_delete(order_id: int, no: int, db: Session = Depends(get_db)):
    query = (
        select(OrderDetail.order_id, OrderDetail.no, Product.name.label("product_name"), OrderDetail.qty)
        .select_from(OrderDetail)
        .outerjoin(Product, OrderDetail.product_id == Product.id)
        .where(OrderDetail.order_id == order_id)
        .where(OrderDetail.no == no)
    )
    orderDetail = get_item(db, query)
    return { "orderDetail": orderDetail }

@router.delete("/orderDetails/{order_id}/{no}")
def delete(order_id: int, no: int, db: Session = Depends(get_db)):
    orderDetail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.no == no).first()
    db.delete(orderDetail)
    db.commit()
