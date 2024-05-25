from fastapi import APIRouter, Depends, status
from app.components.reviews.service import ReviewService
from app.components.reviews.schemas import SReview, SReviewCreate, SReviewUpdate
from app.users.dependencies import get_current_user
from app.users.models import User
from app.exсeptions import UserAlreadyReviewed

router = APIRouter(
    prefix='/reviews',
    tags=["Отзывы"],
)

# Роутер добавляет отзыв
@router.post("/add/{component_id}", response_model=SReview, status_code=status.HTTP_201_CREATED)
async def add_review(component_id: int, review: SReviewCreate, current_user: User = Depends(get_current_user)):
    review_data = review.dict()
    new_review = await ReviewService.create_review(component_id, current_user.id, review_data)
    if new_review is None:
        raise UserAlreadyReviewed
    return new_review

# Роутер редактирует отзыв
@router.put("/edit/{review_id}", response_model=SReview)
async def edit_review(review_id: int, review: SReviewUpdate, current_user: User = Depends(get_current_user)):
    review_data = review.dict(exclude_unset=True)
    updated_review = await ReviewService.update_review(review_id, current_user.id, review_data)
    return updated_review

# Роутер удаляет отзыв
@router.delete("/del/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, current_user: User = Depends(get_current_user)):
    await ReviewService.delete_review(review_id, current_user.id)
    return {"detail": "Отзыв удален"}