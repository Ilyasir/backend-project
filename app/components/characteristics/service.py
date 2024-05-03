from app.services.base import BaseService
from app.database import async_session_maker
from app.components.characteristics.models import Characteristic

from sqlalchemy import select

class CharacteristicService(BaseService):
    model = Characteristic

    # Метод выводит характеристики компонента по id компонента
    @classmethod
    async def get_characteristics(cls, component_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.component_id == component_id)
            result = await session.execute(query)
            characteristics = result.scalars().all()

            formatted_characteristics = {}
            for characteristic in characteristics:
                formatted_characteristics[characteristic.attribute] = characteristic.value
            return formatted_characteristics