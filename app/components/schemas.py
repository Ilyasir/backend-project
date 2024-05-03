from pydantic import BaseModel
from enum import Enum

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
    image_path: str

    class Config:
        orm_mode = True