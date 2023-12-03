import pytest
from fastapi import status
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post("/comment", json={"body": body, "post_id": post_id})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient) -> dict:
    return await create_post("Test post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict) -> dict:
    return await create_comment("Test comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"

    response = await async_client.post(
        "/post",
        json={"body": body},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_without_body_should_return_422_code(async_client: AsyncClient):
    response = await async_client.post(
        "/post",
        json={},
    )

    assert response.status_code == 422
    assert {}.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_all_posts_should_return_list_of_posts_with_status_code_200(
    async_client: AsyncClient, created_post: dict
):
    response = await async_client.get("/post")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test comment"

    response = await async_client.post("/comment", json={"body": body, "post_id": created_post["id"]})

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body, "post_id": created_post["id"]}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_comment_when_post_does_not_exist(async_client: AsyncClient):
    body = "Test comment"

    response = await async_client.post("/comment", json={"body": body, "post_id": -1})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Post not found"}


@pytest.mark.anyio
async def test_get_comments_on_post(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_post_without_comments(async_client: AsyncClient, created_post: dict):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comments(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment],
    }


@pytest.mark.anyio
async def test_get_post_with_comments_when_there_are_no_comments(async_client: AsyncClient, created_post: dict):
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "post": created_post,
        "comments": [],
    }


@pytest.mark.anyio
async def test_get_post_with_comments_when_post_does_not_exist(async_client: AsyncClient):
    response = await async_client.get(f"/post/{-1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Post not found"}
