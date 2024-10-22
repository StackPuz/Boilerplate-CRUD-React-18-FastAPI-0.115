from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from app.config import Base

class UserAccount(Base):
    __tablename__ = "UserAccount"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    password_reset_token = Column(VARCHAR(100))
    active = Column(BIT, nullable=False)
