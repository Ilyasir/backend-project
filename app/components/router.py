from fastapi import APIRouter, Query

from app.components.service import ComponentService
from app.components.schemas import SComponent, TypeComponent
from app.components.characteristics.service import CharacteristicService

router = APIRouter(
    prefix='/catalog',
    tags=["Каталог"],
)

# Роутер выводит все компоненты определенного типа
@router.get("/{type_component}")
async def get_component(
    type_component: TypeComponent, 
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> list[SComponent]:
    components = await ComponentService.find_all(type=type_component)
    return components[offset:offset + limit]

# Роутер выводит характеристики компонента по id компонента
@router.get("/component/{component_id}")
async def get_characteristics(component_id: int):
    return await CharacteristicService.get_characteristics(component_id=component_id)
    

@router.get("/{component_id}")
async def get_characteristics(component_id: int):
    return await CharacteristicService.get_characteristics(component_id=component_id)