from app.dao.base import BaseDAO
from app.users.models import Users


class UserDAO(BaseDAO):
    """id: int, email: str, hashed_password: str"""

    model = Users
