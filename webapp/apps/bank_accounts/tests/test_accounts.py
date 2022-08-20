from django.urls import reverse

import pytest

from ..models import Account, Currency


@pytest.mark.django_db()
class TestAccountsUsecases:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.client = client
        self.url = reverse("bank-accounts:add-account")
        self.currency = Currency.objects.create(symbol="USD")

    def _assert_errors(self, resp, expected_errors):
        assert resp.status_code == 400
        form = resp.context_data["add_account_form"]
        assert form.errors == expected_errors

    def test_add_new_account(self):
        data = {
            "name": "test name 1",
            "description": "test description1",
            "currency": self.currency.id,
            "funds": 0,
        }

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 200
        all_accounts = Account.objects.all()
        assert len(all_accounts) == 1
        assert all_accounts[0].name == data["name"]
        assert all_accounts[0].description == data["description"]
        assert all_accounts[0].currency == self.currency
        assert all_accounts[0].funds == data["funds"]

    def test_add_new_account_and_another_one(self):
        data_1 = {
            "name": "test name 1",
            "description": "test description1",
            "currency_id": self.currency.id,
            "funds": 0,
        }
        data_2 = {
            "name": "test name 2",
            "description": "test description2",
            "currency": self.currency.id,
            "funds": 100,
        }
        Account.objects.create(**data_1)

        resp = self.client.post(self.url, data=data_2)

        assert resp.status_code == 200
        all_accounts = Account.objects.all()
        assert len(all_accounts) == 2
        assert all_accounts[0].name == data_1["name"]
        assert all_accounts[0].description == data_1["description"]
        assert all_accounts[0].currency == self.currency
        assert all_accounts[0].funds == data_1["funds"]
        assert all_accounts[1].name == data_2["name"]
        assert all_accounts[1].description == data_2["description"]
        assert all_accounts[1].currency == self.currency
        assert all_accounts[1].funds == data_2["funds"]

    def test_add_new_account_but_already_exist(self):
        data_1 = {
            "name": "test name 1",
            "description": "test description1",
            "currency_id": self.currency.id,
            "funds": 0,
        }
        data_2 = {
            "name": "test name 1",
            "description": "test description1",
            "currency": self.currency.id,
            "funds": 0,
        }
        expected_errors = {
            "internal": [
                "Cannot add account, 'test name 1' already in database"
            ]
        }
        Account.objects.create(**data_1)

        resp = self.client.post(self.url, data=data_2)

        self._assert_errors(resp, expected_errors)
        all_accounts = Account.objects.all()
        assert len(all_accounts) == 1
        assert all_accounts[0].name == data_2["name"]
        assert all_accounts[0].description == data_2["description"]
        assert all_accounts[0].currency == self.currency
        assert all_accounts[0].funds == data_2["funds"]

    def test_add_new_account_but_missing_data(self):
        data = {}
        expected_errors = {
            "currency": ["This field is required."],
            "description": ["This field is required."],
            "funds": ["This field is required."],
            "name": ["This field is required."],
        }

        resp = self.client.post(self.url, data=data)

        self._assert_errors(resp, expected_errors)
        all_accounts = Account.objects.all()
        assert len(all_accounts) == 0

    def test_add_new_account_but_invalid_funds(self):
        data = {
            "name": "test name 1",
            "description": "test description1",
            "currency": self.currency.id,
            "funds": -1,
        }
        expected_errors = {"funds": ["Value cannot be less than 0"]}

        resp = self.client.post(self.url, data=data)

        self._assert_errors(resp, expected_errors)
        all_accounts = Account.objects.all()
        assert len(all_accounts) == 0

    def test_add_new_account_but_invalid_currency(self):
        data = {
            "name": "test name 1",
            "description": "test description1",
            "currency": 0,
            "funds": 0,
        }
        expected_errors = {
            "currency": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }

        resp = self.client.post(self.url, data=data)

        self._assert_errors(resp, expected_errors)
        all_accounts = Account.objects.all()
        assert len(all_accounts) == 0
