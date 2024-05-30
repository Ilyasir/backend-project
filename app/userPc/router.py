from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi_cache.decorator import cache

from app.userPc.service import UserPcService
from app.userPc.schemas import SUserPc, SCreateUserPc
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
@cache(expire=60)
async def get_user_pcs(user: User = Depends(get_current_user)) -> list[SUserPc]:
    return await UserPcService.find_all(user_id=user.id)

@router.post("", response_model=SUserPc)
async def create_user_pc(
    pc_data: SCreateUserPc,
    user: User = Depends(get_current_user)
):
    try:
        new_pc = await UserPcService.create_user_pc(
            user_id=user.id,
            name=pc_data.name,
            component_ids=pc_data.component_ids
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid component ID")

    return new_pc