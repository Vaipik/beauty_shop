from django.urls import reverse
import pytest
from rest_framework.test import APIClient

from core.user_auth.factories import UserFactory


@pytest.fixture()
def api_client():
    """DRF API client for whole test session."""
    return APIClient()


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


@pytest.fixture(scope="module")
def user_list_url() -> str:
    """Return an url for user-list djoser library."""
    return reverse("user-list")


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


@pytest.fixture(scope="module")
def jwt_create_url():
    """Url to create a jwt."""
    return reverse("jwt-create")


@pytest.fixture(scope="module")
def jwt_refresh_url():
    """Url to refresh a jwt."""
    return reverse("jwt-refresh")
