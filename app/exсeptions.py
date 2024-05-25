from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",                      
)

UserAlreadyReviewed = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже оставил отзыв",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истёк",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует",
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена",
)

UserIsNotInToken =  HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
)

ComponentAlreadyExistsExeption = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Компонент уже существует",
)

ComponentNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Компонент не найден",
)