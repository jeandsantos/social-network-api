from pydantic import BaseModel

from social_network_api.models.comment import Comment


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
