import typing

from django.urls import reverse
from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from core.user_auth.factories import UserFactory

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


@pytest.fixture()
def api_client():
    """DRF API client for whole test session."""
    return APIClient()


"""USERS"""


@pytest.fixture()
def user_sign_up_with_email(db):
    """User which was signed up using email."""
    return UserFactory(
        username="test_user@email.com",
    )


@pytest.fixture()
def user_sign_up_with_phone(db):
    """User which was signed up using phone."""
    return UserFactory(username="0671234567")


@pytest.fixture()
def user_admin_role(db):
    """Create an admin user."""
    return UserFactory(username="admin", role=User.UserRoles.ADMIN)


@pytest.fixture()
def user_manager_role(db):
    """Create a manager user."""
    return UserFactory(username="manager", role=User.UserRoles.MANAGER)


@pytest.fixture()
def user_consultant_role(db):
    """Create a consultant user."""
    return UserFactory(username="consultant", role=User.UserRoles.CONSULTANT)


@pytest.fixture()
def user_customer_role(db):
    """Create a customer user."""
    return UserFactory(username="customer", role=User.UserRoles.CUSTOMER)


@pytest.fixture(scope="module")
def user_sign_up_email_payload() -> dict:
    """Data for sign up using email."""
    return {
        "username": "email@email.com",
        "password": "password",
        "rePassword": "password",
    }


@pytest.fixture(scope="module")
def user_sign_up_phone_payload() -> dict:
    """Data for sign up using phone."""
    return {"username": "0951234567", "password": "password", "rePassword": "password"}


"""URLS"""


@pytest.fixture(scope="module")
def users_list_url() -> str:
    """Return an url for user-list viewset."""
    return reverse("users:users-list")


@pytest.fixture(scope="module")
def users_me_url():
    """Return an url for users/me endpoint."""
    return reverse("users:users-me")


@pytest.fixture(scope="module")
def jwt_create_url():
    """Url to create a jwt."""
    return reverse("jwt-create")


@pytest.fixture(scope="module")
def jwt_refresh_url():
    """Url to refresh a jwt."""
    return reverse("jwt-refresh")


"""auth tokens"""


@pytest.fixture()
def auth_admin_user(api_client, jwt_create_url, user_admin_role):
    """Obtain access token for admin user."""
    return api_client.post(
        path=jwt_create_url,
        data={
            "username": user_admin_role.username,
            "password": "password",  # default factory password
        },
        format="json",
    ).data["access"]


@pytest.fixture()
def auth_customer_user(api_client, jwt_create_url, user_customer_role):
    """Obtain access token for customer user."""
    return api_client.post(
        path=jwt_create_url,
        data={
            "username": user_customer_role.username,
            "password": "password",  # default factory password
        },
        format="json",
    ).data["access"]
