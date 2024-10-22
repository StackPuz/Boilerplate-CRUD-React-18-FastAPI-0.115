from typing import Optional
from app.util import *

class BrandSchema(Model):
    name: str

class BrandUpdateSchema(Model):
    name: str
