import pytest

from ..models import Account, Currency, Transfer
from ..queries import currency_queries, transfer_queries
from .utils import generate_fake_money_value


@pytest.mark.django_db()
class TestBaseQueries:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.query = currency_queries
        self.curr1 = Currency.objects.create(symbol="USD")
        self.curr2 = Currency.objects.create(symbol="EUR")
        self.curr3 = Currency.objects.create(symbol="XXX")

    def test_get_by_id(self):
        currency = self.query.get_by_id(self.curr2.id)
        assert currency == self.curr2

    def test_get_all(self):
        currencies = self.query.get_all()
        assert list(currencies) == [self.curr1, self.curr2, self.curr3]

    def test_count(self):
        assert self.query.count() == 3


@pytest.mark.django_db()
class TestTransferQueries:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.query = transfer_queries
        curr = Currency.objects.create(symbol="USD")
        acc1 = Account.objects.create(name="account 1", currency=curr)
        acc2 = Account.objects.create(name="account 2", currency=curr)
        self.trans1 = Transfer.objects.create(
            name="trx1",
            currency=curr,
            from_account=acc1,
            value=generate_fake_money_value(),
        )
        self.trans2 = Transfer.objects.create(
            name="trx2",
            currency=curr,
            to_account=acc1,
            value=generate_fake_money_value(),
        )
        self.trans3 = Transfer.objects.create(
            name="trx3",
            currency=curr,
            from_account=acc1,
            to_account=acc2,
            value=generate_fake_money_value(),
        )
        self.trans4 = Transfer.objects.create(
            name="trx4",
            currency=curr,
            from_account=acc2,
            to_account=acc1,
            value=generate_fake_money_value(),
        )
        self.trans5 = Transfer.objects.create(
            name="trx5",
            currency=curr,
            from_account=acc2,
            to_account=acc2,
            value=generate_fake_money_value(),
        )
        self.filter_by = acc1

    def test_get_filtered_by_account(self):
        transfers = self.query.get_filtered_by_account(self.filter_by)
        assert list(transfers) == [
            self.trans1,
            self.trans2,
            self.trans3,
            self.trans4,
        ]
