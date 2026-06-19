import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from testcontainers.postgres import PostgresContainer

from models import Base
from repository import CarritoRepositorio

@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:15-alpine") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    # Begin a nested transaction (savepoint)
    transaction = connection.begin()
    
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    
    yield session
    
    session.close()
    # Rollback the transaction to keep DB clean for the next test
    transaction.rollback()
    connection.close()

def test_create_new_cart(db_session: Session):
    repo = CarritoRepositorio(db_session)
    cart = repo.create_cart("session-1")
    
    assert cart is not None
    assert cart.session_id == "session-1"
    assert cart.discount == 0.0

def test_add_same_product_sums_quantity(db_session: Session):
    repo = CarritoRepositorio(db_session)
    session_id = "session-2"
    
    repo.add_item(session_id, "Laptop", 1, 1000.0)
    repo.add_item(session_id, "Laptop", 2, 1000.0)
    
    items = repo.get_items(session_id)
    assert len(items) == 1
    assert items[0].product == "Laptop"
    assert items[0].quantity == 3
    assert items[0].price == 1000.0

def test_calculate_total_with_persisted_data(db_session: Session):
    repo = CarritoRepositorio(db_session)
    session_id = "session-3"
    
    repo.add_item(session_id, "Mouse", 2, 50.0)
    repo.add_item(session_id, "Keyboard", 1, 100.0)
    
    total = repo.get_total(session_id)
    assert total == 200.0
    
    repo.apply_discount(session_id, 10.0)
    total_discounted = repo.get_total(session_id)
    assert total_discounted == 180.0

def test_clear_cart_deletes_items_from_db(db_session: Session):
    repo = CarritoRepositorio(db_session)
    session_id = "session-4"
    
    repo.add_item(session_id, "Monitor", 1, 300.0)
    assert len(repo.get_items(session_id)) == 1
    
    repo.clear_cart(session_id)
    items_after_clear = repo.get_items(session_id)
    
    assert len(items_after_clear) == 0
