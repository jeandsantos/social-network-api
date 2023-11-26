from typing import Union

from fastapi import APIRouter, HTTPException

from social_network_api.models.comment import Comment, CommentIn
from social_network_api.models.post import UserPost, UserPostIn, UserPostWithComments
from social_network_api.typings import CommentType, PostType
from social_network_api.utils import find_post

post_table: dict[int, PostType] = {}
comment_table: dict[int, CommentType] = {}

router = APIRouter()


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn) -> PostType:
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post: PostType = {**data, "id": last_record_id}
    print(new_post)
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts() -> list[PostType]:
    print(list(post_table.values()))
    return list(post_table.values())


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn) -> CommentType:
    post = find_post(post_table, comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    print(new_comment)
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/comment", response_model=list[Comment])
async def get_all_comments() -> list[CommentType]:
    print(list(comment_table.values()))
    return list(comment_table.values())


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int) -> list[CommentType]:
    comments = [comment for comment in comment_table.values() if comment["post_id"] == post_id]
    print(comments)
    return comments


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int) -> dict[str, Union[PostType, list[CommentType]]]:
    post = find_post(post_table, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    output = {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }

    return output
