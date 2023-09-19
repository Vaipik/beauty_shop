from src.utils.phone import is_phone_number_valid


def test_is_phone_number_valid():
    """Validate phone number according to UA rules using regex."""
    valid_number_1 = "0931234567"
    valid_number_2 = "0673215476"
    valid_number_3 = "0917654321"
    not_valid_number_1 = "1931234567"
    not_valid_number_2 = valid_number_2 + "1"
    not_valid_number_3 = valid_number_3[:-1]

    assert is_phone_number_valid(valid_number_1) is True
    assert is_phone_number_valid(valid_number_2) is True
    assert is_phone_number_valid(valid_number_3) is True
    assert is_phone_number_valid(not_valid_number_1) is False
    assert is_phone_number_valid(not_valid_number_2) is False
    assert is_phone_number_valid(not_valid_number_3) is False
