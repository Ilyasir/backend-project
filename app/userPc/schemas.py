# Здесь будут схемы Pydantic
from pydantic import BaseModel

class SUserPc(BaseModel):
    id: int
    user_id: int
    price: int

    class Config:
        orm_mode = True