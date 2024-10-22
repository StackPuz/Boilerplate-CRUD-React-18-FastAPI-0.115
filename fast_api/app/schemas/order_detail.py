from typing import Optional
from app.util import *

class OrderDetailSchema(Model):
    order_id: int
    no: int
    product_id: int
    qty: int

class OrderDetailUpdateSchema(Model):
    product_id: int
    qty: int
