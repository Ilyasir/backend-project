from app.services.base import BaseService
from app.components.models import Component
from app.components.characteristics.models import Characteristic
from app.database import async_session_maker
from sqlalchemy.orm import aliased
from sqlalchemy import select, asc, desc

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

            query = select(Component).where(Component.type == type_component)

            for subquery in subqueries:
                query = query.where(Component.id.in_(select(subquery.c.component_id)))

            if min_price is not None:
                query = query.where(Component.price >= min_price)
            if max_price is not None:
                query = query.where(Component.price <= max_price)

            if order == 1:
                query = query.order_by(asc(Component.price))
            elif order == 2:
                query = query.order_by(desc(Component.price))

            result = await session.execute(query)
            return result.scalars().all()