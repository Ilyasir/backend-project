from fastapi import APIRouter, Query, status
from typing import Optional

from app.components.service import ComponentService
from app.components.schemas import SComponent, STypeComponent, SComponentUpdate
from app.components.characteristics.service import CharacteristicService
from app.components.reviews.schemas import SReview
from app.components.reviews.service import ReviewService

from app.exсeptions import ComponentAlreadyExistsExeption, ComponentNotFound

router = APIRouter(
    prefix='/catalog',
    tags=["Каталог"],
)

# Роутер сортирует и фильтрует все компоненты
@router.post("/", response_model=list[SComponent])
async def filter_components(
    type_component: STypeComponent,
    characteristics: dict[str, str],
    min_price: int = Query(None, ge=0),
    max_price: int = Query(None, ge=0),
    order: int = Query(1, ge=1, le=2),
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100)
):
    components = await ComponentService.filter_components_by_characteristics(
        type_component, characteristics, min_price, max_price, order
    )
    if not components:
        raise ComponentNotFound
    offset_min, offset_max = page * size, (page + 1) * size
    return components[offset_min:offset_max]

# Роутер добавляет новый компонент и его характеристики
@router.post("/add_component")
async def add_component(
    type: STypeComponent,
    name: str,
    price: int,
    characteristics: dict[str, str],
    description: Optional[str] = None,
    image_path: Optional[str] = None
):
    existing_component = await ComponentService.find_one_or_none(name=name)
    if existing_component:
        raise ComponentAlreadyExistsExeption
    component_data = {
        "type": type,
        "name": name,
        "description": description,
        "price": price,
        "image_path": image_path
    }
    component = await ComponentService.add_component(component_data, characteristics)
    return component

# Роутер обновляет компонент и его характеристики
@router.put("/component/{component_id}", response_model=SComponent)
async def update_component(component_id: int, component: SComponentUpdate):
    existing_component = await ComponentService.find_one_or_none(id=component_id)
    if not existing_component:
        raise ComponentNotFound
    component_data = component.dict(exclude_unset=True, exclude={"characteristics"})
    characteristics_data = component.characteristics if component.characteristics is not None else {}
    return await ComponentService.update_component(component_id, component_data, characteristics_data)

# Роутер удаляет компонент и его характеристики
@router.delete("/component/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(component_id: int):
    existing_component = await ComponentService.find_one_or_none(id=component_id)
    if not existing_component:
        raise ComponentNotFound
    await ComponentService.delete_component(component_id)
    return {"detail": "Компонент удален"}

# Роутер выводит характеристики компонента по id компонента
@router.get("/component/{component_id}/characteristics")
async def get_characteristics(component_id: int):
    return await CharacteristicService.get_characteristics(component_id=component_id)

# Роутер выводит отзывы о компоненте по id компонента
@router.get("/component/{component_id}/reviews", response_model=list[SReview])
async def get_reviews(component_id: int):
    reviews = await ReviewService.get_reviews_for_component(component_id)
    return reviews