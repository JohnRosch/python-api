from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Define what a Product looks like using Pydantic
class Product(BaseModel):
    name: str
    price: float

products_db = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Smartphone", "price": 499.99}
}

@app.get("/")
def read_root():
    return {"message": "Welcome to my free hosted API!"}

@app.get("/products")
def get_products():
    return products_db

# 2. Create the POST endpoint to add data
@app.post("/products")
def create_product(product: Product):
    # Generate a new unique ID based on the dictionary size
    new_id = max(products_db.keys()) + 1
    
    # Save the incoming data to our dictionary
    products_db[new_id] = {"name": product.name, "price": product.price}
    
    return {"message": "Product added successfully!", "id": new_id, "data": products_db[new_id]}
