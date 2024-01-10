import pytest

pytestmark = pytest.mark.django_db


def test_sign_up_with_email(api_client, users_list_url, user_sign_up_email_payload):
    """This test perform a sign-up using email as username."""
    r = api_client.post(
        path=users_list_url,
        data=user_sign_up_email_payload,
        format="json",
    )
    assert r.status_code == 201
    assert r.data["username"] == user_sign_up_email_payload["username"]
    assert r.data["email"] == user_sign_up_email_payload["username"]
    assert r.data["phone"] is None


def test_sign_up_with_phone(api_client, users_list_url, user_sign_up_phone_payload):
    """This test perform a sign-up using phon as username."""
    r = api_client.post(
        path=users_list_url,
        data=user_sign_up_phone_payload,
        format="json",
    )
    assert r.status_code == 201
    assert r.data["username"] == user_sign_up_phone_payload["username"]
    assert r.data["phone"] == user_sign_up_phone_payload["username"]
    assert r.data["email"] is None
