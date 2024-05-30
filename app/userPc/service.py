from app.services.base import BaseService
from app.userPc.models import UserPc, UserPcComponent
from app.components.models import Component
from app.database import async_session_maker

class UserPcService(BaseService):
    model = UserPc

    @classmethod
    async def create_user_pc(cls, user_id: int, name: str, component_ids: dict) -> UserPc:
        async with async_session_maker() as session:
            # Считаем цену всех компонентов
            total_price = 0
            components = []
            for component_id in component_ids.values():
                component = await session.get(Component, component_id)
                if not component:
                    raise ValueError(f"Компонент с id {component_id} не существует")
                components.append(component)
                total_price += component.price

            new_pc = UserPc(user_id=user_id, name=name, price=total_price)
            session.add(new_pc)
            await session.commit()
            await session.refresh(new_pc)

            for component in components:
                user_pc_component = UserPcComponent(user_pc_id=new_pc.id, component_id=component.id)
                session.add(user_pc_component)

            await session.commit()
            await session.refresh(new_pc)
            return new_pc