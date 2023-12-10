import pytest

from social_network_api import security


def test_get_password_hash():
    password = "password"
    hashed_password = security.get_password_hash(password)

    assert isinstance(hashed_password, str)
    assert security.verify_password(password, hashed_password)


def test_verify_password():
    password = "password"
    hashed_password = security.get_password_hash(password)

    result = security.verify_password(password, hashed_password)

    assert isinstance(result, bool)
    assert result


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])

    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("non-existing-user@email.com")
    assert user is None
