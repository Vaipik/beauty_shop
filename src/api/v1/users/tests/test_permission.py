import pytest

pytestmark = pytest.mark.django_db


def test_users_list_access(
    api_client, users_list_url, auth_admin_user, auth_customer_user
):
    """Perform a test to check users list permission."""
    # Set admin token
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + auth_admin_user)
    r = api_client.get(
        path=users_list_url,
    )
    assert r.status_code == 200

    # Set customer token
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + auth_customer_user)
    r = api_client.get(
        path=users_list_url,
    )
    assert r.status_code == 403


def test_users_me_access(api_client, users_me_url, auth_admin_user, auth_customer_user):
    """Perform a test to check users list permission."""
    # Set admin token
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + auth_admin_user)
    r = api_client.get(
        path=users_me_url,
    )
    assert r.status_code == 200

    # Set customer token
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + auth_customer_user)
    r = api_client.get(
        path=users_me_url,
    )
    assert r.status_code == 200
