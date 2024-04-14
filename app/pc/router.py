from fastapi import APIRouter, Depends

from app.pc.service import PCService
from app.pc.schemas import SPc
from app.users.models import User
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix='/user_pc', # Будет находится перед всеми эндпоинтами
    tags=["PC"], # Объединение роутеров в группу
)

@router.get("/{pc_id}")
async def get_pc(pc_id: int) -> SPc:
    return await PCService.find_one_or_none(id=pc_id)

# Эндпоинт выводит все PC пользователя
@router.get("")
async def get_user_pcs(user: User = Depends(get_current_user)) -> list[SPc]:
    return await PCService.find_all(user_id=user.id)