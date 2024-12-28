from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestProducts:

    DAO_PATH = 'src.products.router.ProductDAO'

    def test_get_product(self, mock_product_dao):
        with patch(self.DAO_PATH, mock_product_dao):
            response = client.get('/products/1/')
            assert response.status_code == 200
            assert response.json() == mock_product_dao.find_one_or_none.return_value

    def test_delete_product(self, mock_product_dao, get_jwt):
        with patch(self.DAO_PATH, mock_product_dao):
            response = client.delete(
                '/products/1/',
                headers={'Authorization': f'Bearer {get_jwt}'}
            )
            assert response.status_code == 200
            assert response.json() == {'data': 'product 1 deleted successfully'}