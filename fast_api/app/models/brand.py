from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class Brand(Base):
    __tablename__ = "Brand"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
