from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, engine, Base
from repository import CarritoRepositorio

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shopping Cart API")

class ItemCreate(BaseModel):
    product: str
    quantity: int
    price: float

class DiscountApply(BaseModel):
    discount_percentage: float

@app.post("/cart/{session_id}/items")
def add_item_to_cart(session_id: str, item: ItemCreate, db: Session = Depends(get_db)):
    repo = CarritoRepositorio(db)
    cart_item = repo.add_item(session_id, item.product, item.quantity, item.price)
    return {"message": "Item added", "product": cart_item.product, "quantity": cart_item.quantity}

@app.post("/cart/{session_id}/discount")
def apply_discount(session_id: str, discount_data: DiscountApply, db: Session = Depends(get_db)):
    repo = CarritoRepositorio(db)
    repo.apply_discount(session_id, discount_data.discount_percentage)
    return {"message": "Discount applied", "discount": discount_data.discount_percentage}

@app.get("/cart/{session_id}/total")
def get_cart_total(session_id: str, db: Session = Depends(get_db)):
    repo = CarritoRepositorio(db)
    total = repo.get_total(session_id)
    total_with_iva = repo.get_total_with_iva(session_id)
    return {
        "total": total,
        "total_with_iva": total_with_iva
    }

@app.delete("/cart/{session_id}")
def clear_cart(session_id: str, db: Session = Depends(get_db)):
    repo = CarritoRepositorio(db)
    repo.clear_cart(session_id)
    return {"message": "Cart cleared"}
