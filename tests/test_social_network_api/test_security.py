import pytest
from jose import jwt

from social_network_api import security


def test_access_token_expire_minutes():
    result = security.access_token_expire_minutes()

    assert isinstance(result, int)
    assert result > 0


def test_create_access_token():
    token = security.create_access_token("user@email.com")
    assert {"sub": "user@email.com"}.items() <= jwt.decode(
        token,
        key=security.SECRET_KEY,
        algorithms=[security.ALGORITHM],
    ).items()


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


@pytest.mark.anyio
async def test_authenticate_user_with_registered_user(registered_user: dict):
    user = await security.authenticate_user(
        email=registered_user["email"],
        password=registered_user["password"],
    )

    assert user
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_authenticate_user_with_registered_user_and_wrong_password(registered_user: dict):
    with pytest.raises(security.HTTPException):
        await security.authenticate_user(
            email=registered_user["email"],
            password="wrong-password",
        )


@pytest.mark.anyio
async def test_authenticate_user_when_user_does_not_exist():
    with pytest.raises(security.HTTPException):
        await security.authenticate_user("non-existing-user@email.com", "12345")
