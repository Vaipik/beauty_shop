import pytest

pytestmark = pytest.mark.django_db


def test_create_jwt_with_email(api_client, jwt_create_url, user_sign_up_with_email):
    """Obtain jwt tokens using email signed-up credentials."""
    r = api_client.post(
        path=jwt_create_url,
        data={
            "username": user_sign_up_with_email.username,
            "password": "password",  # default password in factory
        },
        format="json",
    )
    assert r.status_code == 200


def test_create_jwt_with_phone(api_client, jwt_create_url, user_sign_up_with_phone):
    """Obtain jwt tokens using phone signed-up credentials."""
    r = api_client.post(
        path=jwt_create_url,
        data={
            "username": user_sign_up_with_phone.username,
            "password": "password",  # default password in factory
        },
        format="json",
    )
    assert r.status_code == 200


def test_create_jwt_with_wrong_credentials(
    api_client, jwt_create_url, user_sign_up_with_phone
):
    """Try to create jwt tokens using phone signed-up user with wrong password."""
    r = api_client.post(
        path=jwt_create_url,
        data={
            "username": user_sign_up_with_phone.username,
            "password": "pass",
        },
        format="json",
    )
    assert r.status_code == 401  # Unauthorized
