from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class OrderHeader(Base):
    __tablename__ = "OrderHeader"
    id = Column(INTEGER, primary_key=True)
    customer_id = Column(INTEGER, nullable=False)
    order_date = Column(DATE, nullable=False)
