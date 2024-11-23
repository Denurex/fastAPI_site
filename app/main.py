import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import datetime
from typing import Optional

import alembic
import uvicorn
from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from app.admins.auth import authentication_backend
from app.admins.views import *
from app.admins.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.database import engine
from app.hotels.hotels_router import router as router_hotels
from app.images.images_router import router as router_images
from app.pages.pages_router import router as router_pages
from app.users.users_router import router as router_users
from app.logger import logger
# from app.users.users_models import Users
import sentry_sdk



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

# sentry_sdk.init(
#     dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
#     traces_sample_rate=1.0,
#     profiles_sample_rate=1.0,
# )

app.mount('/app/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)


origins = ['http://127.0.0.1:5000']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATH', 'PUT'],
                   allow_headers=['Content-Type', 'Set-Cookie',
                                 'Access-control-Allow-Headers', 'Access-Control-Origin',
                                 'Authorization']
                )

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info('Request exec time', extra={
        'process_time': round(process_time,4)
    })
    response.headers["X-Process-Time"] = str(process_time)
    return response

# class SHotel(BaseModel):
#     addres: str
#     name:str
#     stars:int
#
#
# class HotelSearchArgs:
#     def __init__(self,
#                  location: str,
#                  date_from: date,
#                  date_to: date,
#                  has_spa: Optional[bool] = None,
#                  stars: Optional[int] = Query(None, ge=1, le=5)
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars
#
#
# @app.get('/hotels', response_model=list[SHotel])
# def get_hotels(search_args:HotelSearchArgs = Depends()):
#     hotels = [{'addres': 'aaaaaa',
#                'name': 'bbbbbb',
#                'stars': 5
#                }]
#
#     return search_args

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='127.0.0.1', port = 5000, log_level='info')
