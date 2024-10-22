from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class OrderDetail(Base):
    __tablename__ = "OrderDetail"
    order_id = Column(INTEGER, primary_key=True)
    no = Column(SMALLINT, primary_key=True)
    product_id = Column(INTEGER, nullable=False)
    qty = Column(SMALLINT, nullable=False)
