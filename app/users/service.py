from app.services.base import BaseService
from app.users.models import User

class UsersService(BaseService):
    model = User