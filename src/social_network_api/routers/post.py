from typing import Union

from fastapi import APIRouter, HTTPException, status

from social_network_api.database import comment_table, database, post_table
from social_network_api.models.comment import Comment, CommentIn
from social_network_api.models.post import UserPost, UserPostIn, UserPostWithComments
from social_network_api.typings import CommentType, PostType

router = APIRouter()


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@router.post("/post", response_model=UserPost, status_code=status.HTTP_201_CREATED)
async def create_post(post: UserPostIn) -> PostType:
    data = post.model_dump()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentIn) -> CommentType:
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/comment", response_model=list[Comment])
async def get_all_comments():
    query = comment_table.select()
    return await database.fetch_all(query)


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int) -> dict[str, Union[PostType, list[CommentType]]]:
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    output = {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }

    return output
