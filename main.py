import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select
from dotenv import load_dotenv

# 1. Automatically read your local .env file variables
load_dotenv()

# 2. Blueprint schema for our permanent Postgres table
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float

# 3. Get connection string cleanly from environment memory
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing!")

# Fix for Render handling modern postgres drivers securely
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

app = FastAPI()

# 4. Enable browser communication (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create physical database tables inside Neon right when the app turns on
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "My full-stack application is connected to a permanent database!"}

# Endpoint 1: Fetch rows from Postgres database
@app.get("/products")
def get_products():
    with Session(engine) as session:
        statement = select(Product)
        results = session.exec(statement).all()
        # Converts list back to format your frontend code expects
        return {prod.id: {"name": prod.name, "price": prod.price} for prod in results}

# Endpoint 2: Insert new rows securely into Postgres database
@app.post("/products")
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit() # Permanently save to disk drive!
        session.refresh(product) # Pull down auto-incremented primary key ID
        return {"message": "Product saved permanently!", "id": product.id}
