from fastapi import FastAPI

# Импортируем роутеры
from app.userPc.router import router as router_pcs
from app.users.router import router as router_users

app = FastAPI()

# Добавляем к приложению набор эндпоинтов
app.include_router(router_users)
app.include_router(router_pcs)