from app.services.base import BaseService
from app.components.models import Component
from app.components.characteristics.models import Characteristic
from app.database import async_session_maker
from sqlalchemy.orm import aliased, joinedload
from sqlalchemy import select, asc, desc, update, delete

class ComponentService(BaseService):
    model = Component
    
    # Метод сортирует и фильтрует по характеристикам комплектующие
    @classmethod
    async def filter_components_by_characteristics(
        cls,
        type_component,
        characteristics, 
        min_price, 
        max_price,
        order,
    ):
        async with async_session_maker() as session:
            subqueries = []
            for attr, value in characteristics.items():
                alias = aliased(Characteristic)
                subquery = (
                    select(alias.component_id)
                    .where(
                        alias.attribute == attr,
                        alias.value == value
                    )
                    .subquery()
                )
                subqueries.append(subquery)

            query = select(cls.model).options(joinedload(cls.model.characteristic)).where(cls.model.type == type_component)

            for subquery in subqueries:
                query = query.where(cls.model.id.in_(select(subquery.c.component_id)))

            if min_price is not None:
                query = query.where(cls.model.price >= min_price)
            if max_price is not None:
                query = query.where(cls.model.price <= max_price)

            if order == 1:
                query = query.order_by(asc(cls.model.price))
            elif order == 2:
                query = query.order_by(desc(cls.model.price))

            result = await session.execute(query)
            components = result.unique().scalars().all()  # Используем unique() для удаления дубликатов

            # Добавим характеристики к каждому компоненту
            for component in components:
                characteristics_query = select(Characteristic).where(Characteristic.component_id == component.id)
                characteristics_result = await session.execute(characteristics_query)
                characteristics = characteristics_result.scalars().all()
                component.characteristics = {char.attribute: char.value for char in characteristics}

            return components
        
    # Метод добавления компонента и его характеристик
    @classmethod
    async def add_component(cls, component_data, characteristics_data):
        async with async_session_maker() as session:
            component = cls.model(**component_data)
            session.add(component)
            await session.commit()
            for attribute, value in characteristics_data.items():
                characteristic = Characteristic(
                    component_id=component.id,
                    attribute=attribute,
                    value=value
                )
                session.add(characteristic)
            await session.commit()
            await session.refresh(component)
            return component
        

    # Метод обновления компонента и его характеристик
    @classmethod
    async def update_component(cls, component_id, component_data, characteristics_data):
        async with async_session_maker() as session:
            await session.execute(
                update(cls.model)
                .where(cls.model.id == component_id)
                .values(**component_data)
            )
            await session.execute(
                delete(Characteristic).where(Characteristic.component_id == component_id)
            )
            for attribute, value in characteristics_data.items():
                characteristic = Characteristic(
                    component_id=component_id,
                    attribute=attribute,
                    value=value
                )
                session.add(characteristic)
            await session.commit()
            return await session.get(cls.model, component_id)

    # Метод удаления компонента и его характеристик
    @classmethod
    async def delete_component(cls, component_id):
        async with async_session_maker() as session:
            await session.execute(
                delete(Characteristic).where(Characteristic.component_id == component_id)
            )
            await session.execute(
                delete(Component).where(Component.id == component_id)
            )
            await session.commit()