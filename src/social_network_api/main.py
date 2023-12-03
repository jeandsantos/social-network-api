import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from social_network_api.database import database
from social_network_api.logging_conf import configure_logging
from social_network_api.routers import post

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Connecting database")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello world!"}
