from fastapi import APIRouter, HTTPException

from app.users.schemas import SUserRegister
from app.users.service import UsersService
from app.users.auth import get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

# Эндпоинт для регистрации пользователя
@router.post("/register")
async def register_user(user_data: SUserRegister):
    # Находим юзера по email
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user: # Если он уже есть в БД, то выводим ошибку
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password) # Создаём хэшированный пароль
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)
    return 'Пользователь зарегистрирован', await UsersService.find_one_or_none(email=user_data.email)