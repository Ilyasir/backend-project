from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict

class STypeComponent(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    mb = "mb"
    ram = "ram"
    memory = "memory"
    power = "power"
    cooler = "cooler"
    case = "case"

class STypeSort(str, Enum):
    price_asc = "1"
    price_desc = "2"
    num_reviews = "3"
    rating_asc = "4"
    rating_desc = "5"

class SComponentUpdate(BaseModel):
    type: Optional[STypeComponent]
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    image_path: Optional[str]
    characteristics: Optional[Dict[str, str]]

    class Config:
        orm_mode = True

class SComponent(BaseModel):
    id: int
    type: STypeComponent
    name: str
    description: Optional[str]
    price: int
    image_path: Optional[str] = None

    class Config:
        orm_mode = True