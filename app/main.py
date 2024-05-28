from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Импортируем роутеры
from app.userPc.router import router as router_user_pcs
from app.users.router import router as router_users
from app.components.router import router as router_component
from app.components.reviews.router import router as router_reviews

# Добавляем к приложению набор эндпоинтов
app.include_router(router_users)
app.include_router(router_user_pcs)
app.include_router(router_component)
app.include_router(router_reviews)