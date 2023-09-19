import re


def is_phone_number_valid(number: str) -> bool:
    """Perform a validation of mobile phone number.

    Validation is perforemd due to Ukrainian cell operators.

    See: https://www.vodafone.ua/support/faq/jak-diznatysj-kod-operatora
    :param number: string with phone number which should be validated
    :return: True if number is valid and False if it is not.
    """
    pattern = r"^(050|066|095|099|067|068|096|097|098|063|073|093|091|092|094)\d{7}$"
    match = re.match(pattern, number)
    return True if match else False
