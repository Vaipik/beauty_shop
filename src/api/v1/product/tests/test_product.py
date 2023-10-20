def test_product(product):
    """Test function"""
    product = product(main_card=True)
    assert product.status == product.ProductStatusChoices.IN_STOCK
