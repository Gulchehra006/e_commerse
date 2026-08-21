from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.products import Product
from app.models.favourite import Favourite
from app.schemas.favourite import ResponseFavourite, CreateFavourite
from app.utils.checked_ident import check_id
from app.utils.security import get_current_user

router = APIRouter(tags=["Favorite"], prefix="/favorite")


@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_favorite(data: CreateFavourite, db: Annotated[AsyncSession, Depends(get_db)], current_user=Depends(get_current_user)):
    await check_id(db, Product, data.product_id)

    result = await db.execute(
        select(Favourite).where(
            Favourite.user_id == current_user.id,
            Favourite.product_id == data.product_id
        )
    )

    already_exists = result.scalars().first()

    if already_exists:
        await db.delete(already_exists)
        await db.commit()
        return {"message": "Favourite item was successfully deleted"}

    obj = Favourite(
        user_id=current_user.id,
        product_id=data.product_id
    )

    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return {"message": "Favourite item was successfully added"}


@router.get("/", response_model=list[ResponseFavourite])
async def get_my_favorites(db: Annotated[AsyncSession, Depends(get_db)], current_user=Depends(get_current_user)):
    result = await db.execute(
        select(Favourite).where(
            Favourite.user_id == current_user.id
        )
    )

    favorites = result.scalars().all()

    return favorites