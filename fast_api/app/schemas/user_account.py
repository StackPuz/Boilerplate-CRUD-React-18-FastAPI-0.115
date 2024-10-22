from typing import Optional
from app.util import *

class UserAccountSchema(Model):
    name: str
    email: str
    active: Optional[bool] = None

class UserAccountUpdateSchema(Model):
    name: str
    email: str
    password: Optional[str] = None
    active: Optional[bool] = None
