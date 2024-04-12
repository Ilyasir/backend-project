from fastapi import APIRouter, HTTPException, status, Response

from app.users.schemas import SUserAuth
from app.users.service import UsersService
from app.users.auth import get_password_hash
from app.users.auth import authenticate_user
from app.users.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

# Эндпоинт для регистрации пользователя
@router.post("/register")
async def register_user(user_data: SUserAuth):
    # Находим юзера по email
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user: # Если он уже есть в БД, то выводим ошибку
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    hashed_password = get_password_hash(user_data.password) # Создаём хэшированный пароль
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)
    return 'Пользователь зарегистрирован', await UsersService.find_one_or_none(email=user_data.email)

# Эндпоинт для входа пользователя
@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user: # Если такого пользователя нет
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Создаём токен JWT
    access_token = create_access_token({"sub": str(user.id)})
    # Отправляем в cokkie
    response.set_cookie("pc_access_token", access_token, httponly=True)
    return {"access_token": access_token}