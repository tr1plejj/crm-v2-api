from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.auth.router import router as auth_router
from src.crm.router import router as crm_router
from redis import asyncio as aioredis

app = FastAPI()
app.include_router(auth_router)
app.include_router(crm_router)

@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')