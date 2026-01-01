from sqlalchemy import *
from sqlalchemy.orm import *


Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer , primary_key = True , index = True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)