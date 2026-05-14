import pytest
from cart import Cart

def test_new_cart_is_empty():
    cart = Cart()
    assert cart.items == {}

def test_no_agregar_mas_del_stock_disponible():
    cart = Cart()
    stock_en_tienda = 5
    with pytest.raises(ValueError, match="No hay suficiente stock"):
        cart.add_item("manzana", 6, stock_en_tienda)

def test_agregar_item_con_stock_suficiente():
    cart = Cart()
    stock_en_tienda = 10
    cart.add_item("manzana", 3, stock_en_tienda)
    assert cart.items == {"manzana": 3}

def test_vaciar_el_carrito():
    cart = Cart()
    cart.add_item("manzana", 3, 10)
    cart.add_item("pera", 2, 5)
    
    cart.clear()
    assert cart.items == {}
