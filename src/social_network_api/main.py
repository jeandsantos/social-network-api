from typing import Union

from fastapi import FastAPI

from social_network_api.routers import post

post_table: dict[int, dict[str, Union[str, int]]] = {}

app = FastAPI()
app.include_router(post.router, prefix="/posts")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello world!"}
