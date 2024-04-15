# Здесь будут хранится: модели sqlalchemy, pydantic-схемы для валидации данных, эндпоинты
from sqlalchemy import Column, Integer, String
from app.database import Base

# Таблица с информацией о пользователях
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)