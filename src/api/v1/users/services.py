from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(data: dict) -> User:
    """Create user with phone or email as username.

    Define email or phone was provided in username field.
    :param data: dictionary with two validated fields: username and raw password
    :return:
    """
    username = data["username"]
    password = data["password"]

    if "@" in username:
        user = User.objects.create_user(
            username=username, email=username, password=password
        )
    else:
        user = User.objects.create_user(
            username=username, phone=username, password=password
        )

    return user
