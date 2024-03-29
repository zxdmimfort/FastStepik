from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException, UserNotEnoughPermissions
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str, admin: bool = False):
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        raise IncorrectEmailOrPasswordException
    if admin and not user.admin:
        raise UserNotEnoughPermissions
    if verify_password(password, user.hashed_password):
        return user
    else:
        raise IncorrectEmailOrPasswordException
