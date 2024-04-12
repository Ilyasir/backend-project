from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr

from app.config import settings
from app.users.service import UsersService


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
# Функция для хэширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
# Функция для верификации пароля
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Функция для создания JWT токена, который будем отдавать юзеру
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

# Функция проверяет, есть ли пользователь с таким email и паролем
async def authenticate_user(email: EmailStr, password: str):
    user = await UsersService.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user