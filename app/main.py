from fastapi import FastAPI

# Импортируем роутеры
from app.userPc.router import router as router_user_pcs
from app.users.router import router as router_users
from app.components.router import router as router_component

app = FastAPI()

# Добавляем к приложению набор эндпоинтов
app.include_router(router_users)
app.include_router(router_user_pcs)
app.include_router(router_component)