from app.services.base import BaseService
from app.components.reviews.models import Review
from app.database import async_session_maker
from sqlalchemy import select, update, delete

class ReviewService(BaseService):
    model = Review

    # Метод добавляет отзыв
    @classmethod
    async def create_review(cls, component_id: int, user_id: int, review_data):
        async with async_session_maker() as session:
            existing_review = await session.execute(
                select(cls.model).where(cls.model.component_id == component_id, cls.model.user_id == user_id)
            )
            if existing_review.scalar():
                return None  # Review already exists
            review = cls.model(component_id=component_id, user_id=user_id, **review_data)
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review

    # Метод получает отзывы на комплектующую
    @classmethod
    async def get_reviews_for_component(cls, component_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model).where(cls.model.component_id == component_id)
            )
            return result.scalars().all()
    
    # Метод обновляет отзыв
    @classmethod
    async def update_review(cls, review_id: int, user_id: int, review_data):
        async with async_session_maker() as session:
            result = await session.execute(
                update(cls.model)
                .where(cls.model.id == review_id, cls.model.user_id == user_id)
                .values(**review_data)
                .returning(cls.model)
            )
            review = result.scalar()
            if review:
                await session.commit()
                return review
            else:
                await session.rollback()
                return None

    # Метод удаляет отзыв
    @classmethod
    async def delete_review(cls, review_id: int, user_id: int):
        async with async_session_maker() as session:
            await session.execute(delete(cls.model).where(cls.model.id == review_id, cls.model.user_id == user_id))
            await session.commit()