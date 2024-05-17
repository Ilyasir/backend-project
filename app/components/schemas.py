from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TypeComponent(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    mb = "mb"
    ram = "ram"
    memory = "memory"
    power = "power"
    cooler = "cooler"
    case = "case"

class SComponent(BaseModel):
    id: int
    type: TypeComponent
    name: str
    description: str
    price: int
    image_path: Optional[str] = None

    class Config:
        orm_mode = True