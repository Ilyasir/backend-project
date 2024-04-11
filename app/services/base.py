# В этом файле будут часто используемые методы для взаимодействия с базой данных

from app.database import async_session_maker # Импортируем генератор сессий
from sqlalchemy import select, insert

class BaseService:
    model = None

    # Метод, который фильтрует строки
    @classmethod # Чтобы не создавать каждый раз экземпляр класса
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by) # Запрос, который возвращает PC по фильтрам
            result = await session.execute(query) # Исполняет запрос
            return result.mappings().all() # Возвращает все записи в JSON
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Метод, который возвращает строку по id
    @classmethod
    async def find_by_id(cls, model_id:int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    # Метод, который добавляет новую строчку в БД
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data) # Запрос вставляет данные
            await session.execute(query)
            await session.commit() # Фиксируем изменения в БД