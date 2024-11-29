from decimal import Decimal

from fastapi import status
import pytest

from app.models import Receipt


class TestReceipts:
    receipt_post_data = {
        "products": [
            {
                "name": "product_3",
                "price": 1,
                "quantity": 2,
                "add_field_1": "test_1",
                "add_field_2": "test_2"
            },
            {
                "name": "product_2",
                "price": 0.2,
                "quantity": 20,
                "add_field_3": "test_3"
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 100
        }
    }

    def test_create_receipt(self, authorized_client, db_session):
        api_client, registered_client = authorized_client
        response = api_client.post("/receipts", json=self.receipt_post_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert type(response_data['id']) == str
        total = Decimal(1 * 2 + 0.2 * 20)
        assert Decimal(response_data['total']) == total
        assert Decimal(response_data['rest']) == 100 - total
        assert db_session.query(Receipt).count() == 1

    def test_create_receipt_for_non_authorized_client(self, api_client, db_session):
        response = api_client.post("/receipts", json=self.receipt_post_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['detail'] == 'Not authenticated'
        assert db_session.query(Receipt).count() == 0
