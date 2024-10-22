from datetime import *
from typing import Optional
from app.util import *

class OrderHeaderSchema(Model):
    customer_id: int
    order_date: date

class OrderHeaderUpdateSchema(Model):
    customer_id: int
    order_date: date
