from typing import Union

from fastapi import APIRouter

from social_network_api.models.post import UserPost, UserPostIn

post_table: dict[int, dict[str, Union[str, int]]] = {}

router = APIRouter()


@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn) -> dict[str, Union[str, int]]:
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts(post: UserPostIn) -> list[dict[str, Union[str, int]]]:
    return list(post_table.values())
