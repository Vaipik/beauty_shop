import pytest

from core.product import factories


@pytest.fixture()
def product():
    def inner(**kwargs):
        return factories.ProductFactory(**kwargs)

    return inner


@pytest.fixture()
def product_status(status: str) -> str:
    """"""
    return {
        "in_stock": "I",
        "out_of_stock": "O",
        "expected": "P",
    }.get(status)
