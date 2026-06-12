from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ⚠️ MANDATORY FOR FRONTEND: Allow your browser to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any local HTML file to access the data
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/products")
def create_product(product: Product):
    new_id = max(products_db.keys()) + 1 if products_db else 1
    products_db[new_id] = {"name": product.name, "price": product.price}
    return {"message": "Product added successfully!", "id": new_id, "data": products_db[new_id]}