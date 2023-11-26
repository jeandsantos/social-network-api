from typing import TypedDict


class PostType(TypedDict):
    body: str
    id: int


class CommentType(TypedDict):
    body: str
    post_id: int
    id: int
