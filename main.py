
from fastapi import *
from models import Product
from database import *
import database_models
from fastapi.middleware.cors import *



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

database_models.Base.metadata.create_all(bind = engine)

@app.get("/")
def greet():
    return ("Hello Welcome to the FASTAPI-Project")

products = [
    Product(id = 1,name = "Phone",description = "very good",price = 1000,quantity = 12),
    Product(id = 2,name = "Laptop",description = "powerful",price = 9000,quantity = 5),
    Product(id = 3,name = "Tv ",description = "Entertainment",price = 5000,quantity = 2),
    Product(id = 4,name = "fridge",description = "cooling",price = 7000,quantity = 1)    
]


def inti_db():
    db = SessionLocal()
    count = db.query(database_models.Product).count()
    if (count == 0):
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

inti_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_Id(id: int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product Not found"

@app.post("/products")
def add_product(prod : Product,db:Session = Depends(get_db)):
    db_product = db.add(database_models.Product(**prod.model_dump()))
    db.commit()
    return "product added successfully"


@app.put("/products/{id}")
def update_product(id:int,product : Product,db:Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    else:
        return "Product Not Found"

@app.delete("/products/{id}")
def delete_product(id : int,db:Session = Depends(get_db)):
    
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted Successfully"
    else:
        return "Product Not found"
