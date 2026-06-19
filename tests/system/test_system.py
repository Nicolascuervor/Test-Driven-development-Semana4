import pytest
import httpx

BASE_URL = "http://localhost:8000"

def test_system_add_and_clear_cart():
    session_id = "sys-session-1"
    
    # Ensure cart is clean
    httpx.delete(f"{BASE_URL}/cart/{session_id}")
    
    # Add product
    response = httpx.post(
        f"{BASE_URL}/cart/{session_id}/items",
        json={"product": "TV", "quantity": 1, "price": 500.0}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Item added"
    
    # Check total
    response = httpx.get(f"{BASE_URL}/cart/{session_id}/total")
    assert response.status_code == 200
    assert response.json()["total"] == 500.0
    
    # Clear cart
    response = httpx.delete(f"{BASE_URL}/cart/{session_id}")
    assert response.status_code == 200
    
    # Check total again
    response = httpx.get(f"{BASE_URL}/cart/{session_id}/total")
    assert response.json()["total"] == 0.0

def test_system_discount_and_iva():
    session_id = "sys-session-2"
    httpx.delete(f"{BASE_URL}/cart/{session_id}")
    
    # Add products
    httpx.post(f"{BASE_URL}/cart/{session_id}/items", json={"product": "Phone", "quantity": 2, "price": 300.0})
    
    # Apply discount 10% -> 60 off, total 540
    response = httpx.post(f"{BASE_URL}/cart/{session_id}/discount", json={"discount_percentage": 10.0})
    assert response.status_code == 200
    
    # Verify total and total_with_iva
    response = httpx.get(f"{BASE_URL}/cart/{session_id}/total")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 540.0
    # 540 * 1.19 = 642.6
    assert abs(data["total_with_iva"] - 642.6) < 0.01

def test_system_sessions_do_not_mix():
    session_A = "sys-session-A"
    session_B = "sys-session-B"
    httpx.delete(f"{BASE_URL}/cart/{session_A}")
    httpx.delete(f"{BASE_URL}/cart/{session_B}")
    
    # Add to A
    httpx.post(f"{BASE_URL}/cart/{session_A}/items", json={"product": "Book", "quantity": 1, "price": 20.0})
    # Add to B
    httpx.post(f"{BASE_URL}/cart/{session_B}/items", json={"product": "Pen", "quantity": 5, "price": 2.0})
    
    # Total A should be 20, Total B should be 10
    total_A = httpx.get(f"{BASE_URL}/cart/{session_A}/total").json()["total"]
    total_B = httpx.get(f"{BASE_URL}/cart/{session_B}/total").json()["total"]
    
    assert total_A == 20.0
    assert total_B == 10.0
