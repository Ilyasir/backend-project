from fastapi import FastAPI, Query
from pydantic import BaseModel

# Импортируем роутер
from app.pc.router import router as router_pcs

app = FastAPI()

# Добавляем к приложению набор эндпоинтов
app.include_router(router_pcs)