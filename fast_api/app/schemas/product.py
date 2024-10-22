from decimal import Decimal
from typing import Optional
from app.util import *

@form_body
class ProductSchema(Model):
    name: str
    price: Decimal
    brand_id: int
    image: Optional[str] = None

@form_body
class ProductUpdateSchema(Model):
    name: str
    price: Decimal
    brand_id: int
    image: Optional[str] = None
