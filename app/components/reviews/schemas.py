from pydantic import BaseModel, Field
from typing import Optional

class SReview(BaseModel):
    id: int
    component_id: int
    user_id: Optional[int] = None
    rating: int = Field(le=5, ge=1)
    comment: Optional[str] = None

    class Config:
        orm_mode = True

class SReviewCreate(BaseModel):
    rating: int = Field(le=5, ge=1)
    comment: Optional[str] = None

class SReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, le=5, ge=1)
    comment: Optional[str] = None