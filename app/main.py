import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.database.connection import engine
from app.database.base import Base
from app.routers.category import router as category_router
from app.routers.products import router as product_router
from app.routers.media import router as media_router
from app.routers.variant import router as variant_router
from app.routers.option import router as option_router
from app.routers.local_auth import router as local_auth_router
from app.routers.google_oauth import router as google_auth_router
from app.routers.save_file import router as save_image_file
from app.routers.favourite import router as favourite
from app.routers.review import router as review_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Loyiha",
    docs_url="/",
    lifespan=lifespan
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

app.include_router(local_auth_router)
app.include_router(google_auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(media_router)
app.include_router(variant_router)
app.include_router(option_router)
app.include_router(save_image_file)
app.include_router(favourite)
app.include_router(review_router)

add_pagination(app)

