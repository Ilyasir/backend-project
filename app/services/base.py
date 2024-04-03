# В этом файле будут часто используемые методы для взаимодействия с базой данных

from app.database import async_session_maker # Импортируем генератор сессий
from sqlalchemy import select

class BaseService:
    model = None

    @classmethod # Чтобы не создавать каждый раз экземпляр класса
    # Метод, который выводит все пк
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model) # Запрос, который возвращает все pc (равносильно SELECT * FROM pc;)
            result = await session.execute(query) # Исполняет запрос
            return result.mappings().all() # Возвращает все записи в JSON