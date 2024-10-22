from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class UserRole(Base):
    __tablename__ = "UserRole"
    user_id = Column(INTEGER, primary_key=True)
    role_id = Column(INTEGER, primary_key=True)
