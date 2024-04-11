from fastapi import APIRouter

from app.pc.service import PCService
from app.pc.schemas import SPc

router = APIRouter(
    prefix='/user_pc', # Будет находится перед всеми эндпоинтами
    tags=["PC"], # Объединение роутеров в группу
)

@router.get("/{pc_id}")
async def get_pcs(pc_id: int) -> SPc:
    return await PCService.find_one_or_none(id=pc_id)