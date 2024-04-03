from fastapi import APIRouter

from app.pc.service import PCService

router = APIRouter(
    prefix='/user_pc', # Будет находится перед всеми эндпоинтами
    tags=["Готовые сборки"], # Объединение роутеров в группу
)

@router.get("")
async def get_pcs():
    return await PCService.find_all()