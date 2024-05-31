# Здесь будут схемы Pydantic
from pydantic import BaseModel
from typing import Dict

class SUserPc(BaseModel):
    id: int
    name: str
    user_id: int
    price: int

    class Config:
        orm_mode = True

class SCreateUserPc(BaseModel):
    name: str
    component_ids: Dict[str, int]

    class Config:
        orm_mode = True