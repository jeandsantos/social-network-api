import pytest
from fastapi import status
from httpx import AsyncClient


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/register",
        json={
            "email": email,
            "password": password,
        },
    )


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(async_client, "user@email.com", "12345")
    assert response.status_code == status.HTTP_201_CREATED
    assert "User created" in response.json()["detail"]


@pytest.mark.anyio
async def test_register_user_when_user_already_exists(
    async_client: AsyncClient,
    registered_user: dict,
):
    response = await register_user(
        async_client,
        registered_user["email"],
        registered_user["password"],
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_when_user_exists(async_client: AsyncClient, registered_user: dict):
    response = await async_client.post(
        "/token",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_login_when_user_does_not_exist(async_client: AsyncClient):
    response = await async_client.post(
        "/token",
        json={
            "email": "non-existing-user@email.com",
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate credentials" in response.json()["detail"]
