from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class Role(Base):
    __tablename__ = "Role"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
