from sqlalchemy.orm import *
from sqlalchemy import *

db_url = "postgresql://postgres:Pa77word@localhost:5432/fastdb"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)