from sqlalchemy.orm import Session
from models import Cart, CartItem

class CarritoRepositorio:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_cart(self, session_id: str) -> Cart:
        cart = self.db.query(Cart).filter(Cart.session_id == session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    def get_cart(self, session_id: str) -> Cart:
        return self.db.query(Cart).filter(Cart.session_id == session_id).first()

    def add_item(self, session_id: str, product: str, quantity: int, price: float) -> CartItem:
        # Asegurar que el carrito exista
        self.create_cart(session_id)
        
        item = self.db.query(CartItem).filter(
            CartItem.session_id == session_id,
            CartItem.product == product
        ).first()
        
        if item:
            item.quantity += quantity
        else:
            item = CartItem(session_id=session_id, product=product, quantity=quantity, price=price)
            self.db.add(item)
            
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_items(self, session_id: str) -> list[CartItem]:
        return self.db.query(CartItem).filter(CartItem.session_id == session_id).all()

    def apply_discount(self, session_id: str, discount: float):
        cart = self.get_cart(session_id)
        if cart:
            cart.discount = discount
            self.db.commit()

    def get_total(self, session_id: str) -> float:
        items = self.get_items(session_id)
        cart = self.get_cart(session_id)
        
        subtotal = sum(item.price * item.quantity for item in items)
        
        if cart and cart.discount > 0:
            subtotal -= subtotal * (cart.discount / 100)
            
        return subtotal

    def get_total_with_iva(self, session_id: str, iva_rate: float = 0.19) -> float:
        total = self.get_total(session_id)
        return total * (1 + iva_rate)

    def clear_cart(self, session_id: str):
        self.db.query(CartItem).filter(CartItem.session_id == session_id).delete()
        self.db.commit()
