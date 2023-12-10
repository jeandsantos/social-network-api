import logging

from social_network_api.database import database, user_table

logger = logging.getLogger(__name__)


async def get_user(email: str):
    logging.debug("Fetching user from database", extra={"email": email})
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result
