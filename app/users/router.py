from fastapi import APIRouter, Response, Depends

from app.users.schemas import SUserAuth
from app.users.schemas import SUserReg
from app.users.service import UsersService
from app.components.reviews.service import ReviewService
from app.components.reviews.schemas import SReview
from app.users.auth import get_password_hash
from app.users.auth import authenticate_user
from app.users.auth import create_access_token
from app.users.dependencies import get_current_user
from app.users.models import User
from app.exсeptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

# Роутер для регистрации пользователя
@router.post("/register")
async def register_user(user_data: SUserReg):
    # Находим юзера по email
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user: # Если он уже есть в БД, то выводим ошибку
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password) # Создаём хэшированный пароль
    await UsersService.add(email=user_data.email, hashed_password=hashed_password, username=user_data.username)
    return 'Пользователь зарегистрирован', await UsersService.find_one_or_none(email=user_data.email)

# Роутер для входа пользователя
@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user: # Если такого пользователя нет
        raise IncorrectEmailOrPasswordException
    # Создаём токен JWT
    access_token = create_access_token({"sub": str(user.id)})
    # Отправляем в cokkie
    response.set_cookie("userpc_access_token", access_token, httponly=True)
    return "Пользователь вошёл", {"access_token": access_token}

# Роутер для выхода пользователя
@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("userpc_access_token")
    return "Пользователь вышел"

# Роутер выводит информацию о пользователе
@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Роутер выводит все отзывы пользователя
@router.get("/me/reviews")
async def get_user_reviews(user: User = Depends(get_current_user)) -> list[SReview]:
    return await ReviewService.find_all(user_id=user.id)