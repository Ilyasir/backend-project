from fastapi import APIRouter, Depends

from app.userPc.service import UserPcService
from app.userPc.schemas import SUserPc
from app.users.models import User
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix='/user_pc', # Будет находится перед всеми эндпоинтами
    tags=["Компьютеры пользователя"], # Объединение роутеров в группу
)

@router.get("/{pc_id}")
async def get_pc(pc_id: int) -> SUserPc:
    return await UserPcService.find_one_or_none(id=pc_id)

# Роутер выводит все PC пользователя
@router.get("")
async def get_user_pcs(user: User = Depends(get_current_user)) -> list[SUserPc]:
    return await UserPcService.find_all(user_id=user.id)