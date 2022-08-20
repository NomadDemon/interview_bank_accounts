import random
from decimal import Decimal


def funds_to_decimal(value):
    return Decimal(str(value))


def generate_fake_money_value():
    rand_value = str(round(random.uniform(0.01, 100), 2))
    return Decimal(rand_value)
