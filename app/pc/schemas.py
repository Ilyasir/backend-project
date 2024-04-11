# Здесь будут схемы Pydantic
from pydantic import BaseModel
from typing import Optional

class SPc(BaseModel):
    id: int
    name: str
    is_gaming: Optional[bool] = None
    cpu_id: int
    user_id: int
    image_id: Optional[int] = None

    class Config:
        orm_mode = True