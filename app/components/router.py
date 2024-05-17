from fastapi import APIRouter, Query
from app.components.service import ComponentService
from app.components.schemas import SComponent, TypeComponent
from app.components.characteristics.service import CharacteristicService

router = APIRouter(
    prefix='/catalog',
    tags=["Каталог"],
)

# Роутер сортирует и фильтрует все компоненты
@router.post("/{type_component}", response_model=list[SComponent])
async def filter_components(
    type_component: TypeComponent,
    characteristics: dict[str, str],
    min_price: int = Query(None, ge=0),
    max_price: int = Query(None, ge=0),
    order: int = Query(1, ge=1, le=2),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    components = await ComponentService.filter_components_by_characteristics(
        type_component, characteristics, min_price, max_price, order
    )
    return components[offset:offset + limit]

# Роутер выводит характеристики компонента по id компонента
@router.get("/component/{component_id}")
async def get_characteristics(component_id: int):
    return await CharacteristicService.get_characteristics(component_id=component_id)