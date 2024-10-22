from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class Product(Base):
    __tablename__ = "Product"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    brand_id = Column(INTEGER, nullable=False)
    image = Column(VARCHAR(50))
    create_user = Column(INTEGER)
    create_date = Column(DATETIME)
