from decimal import Decimal

from fastapi import status
import pytest

from app.models import Receipt


class TestReceipts:
    receipt_post_data = {
        "products": [
            {
                "name": "product_1",
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
    total = Decimal(1 * 2 + 0.2 * 20)

    def test_create_receipt(self, authorized_client, db_session):
        api_client, _registered_client = authorized_client
        response = api_client.post("/receipts", json=self.receipt_post_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert type(response_data['id']) == str
        assert Decimal(response_data['total']) == self.total
        assert Decimal(response_data['rest']) == 100 - self.total
        assert db_session.query(Receipt).count() == 1

    def test_create_receipt_for_non_authorized_client(self, api_client, db_session):
        response = api_client.post("/receipts", json=self.receipt_post_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['detail'] == 'Not authenticated'
        assert db_session.query(Receipt).count() == 0

    def test_get_receipt(self, authorized_client, receipt):
        api_client, _registered_client = authorized_client
        response = api_client.get(f"/receipts/{receipt.id}")
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response_data['total']) == receipt.total
        assert Decimal(response_data['rest']) == receipt.rest

    def test_get_receipt_preview_for_non_authorized_client(self, api_client, receipt):
        response = api_client.get(f"/receipts/{receipt.id}/preview/")
        assert response.status_code == status.HTTP_200_OK
        response_text = response.text
        assert "product_1" in response_text
        assert "add_field_3" in response_text

