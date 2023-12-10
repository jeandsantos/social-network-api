import datetime
import logging

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from social_network_api.database import database, user_table

logger = logging.getLogger(__name__)


SECRET_KEY = "9b73f2a1bdd7ae163444473d29a6885ffa22ab26117068£72a5a56a74d12d1fc"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def access_token_expire_minutes() -> int:
    return 60


def create_access_token(email: str):
    logger.debug("Creating access token", extra={"email": email})
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=access_token_expire_minutes())
    jwt_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    logging.debug("Fetching user from database", extra={"email": email})
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result


async def authenticate_user(email: str, password: str):
    logger.debug("Authenticating user", extra={"email": email})
    user = await get_user(email)
    if not user:
        raise credentials_exception
    if not verify_password(password, user.password):
        raise credentials_exception
    return user
