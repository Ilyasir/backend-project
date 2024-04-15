from fastapi import HTTPException, status, Request, Depends
from jose import jwt, JWTError
from datetime import datetime

from app.users.service import UsersService
from app.config import settings
from app.exсeptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, UserIsNotInToken

def get_token(request: Request):
    token = request.cookies.get("userpc_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)): # Ссылаемся на функцию get_token
    try:
        # Декодируем JWT токен
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotInToken
    user = await UsersService.find_by_id(int(user_id))
    if not user_id:
        raise UserIsNotInToken
    return user