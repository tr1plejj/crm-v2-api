import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_product_dao():
    with patch('src.products.dao.ProductDAO') as MockDAO:
        dao = MockDAO()
        dao.find_one_or_none = AsyncMock(return_value={"id": 1, "seller_id": 1, "title": "string", "price": 0, "amount": 100, "description": "string"})
        dao.delete = AsyncMock(return_value={"id": 1, "seller_id": 1, "title": "string", "price": 0, "amount": 100, "description": "string"})
        yield dao

@pytest.fixture
def get_jwt():
    response = client.post(
        '/auth/jwt/login',
        data={'username': 'user@example.com', 'password': 'string'}
    )
    assert response.status_code == 200
    return response.json()['access_token']




