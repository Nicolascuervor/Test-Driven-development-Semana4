from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Cart(Base):
    __tablename__ = "carts"
    
    session_id = Column(String, primary_key=True, index=True)
    discount = Column(Float, default=0.0)

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("carts.session_id"), nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
