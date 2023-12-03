from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI

from social_network_api.database import database
from social_network_api.routers import post


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello world!"}
