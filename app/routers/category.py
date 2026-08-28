from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.category import Category
from app.schemas.category import CreateCategory, ResponseCategory
from app.utils.security import get_current_user

router = APIRouter(tags=['Category'], prefix="/category")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseCategory)
async def add_category(data: CreateCategory , db: Annotated[AsyncSession, Depends(get_db)],
                       current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = Category(name=data.name)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/")
async def get_category(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    category = result.scalars().all()
    return category


@router.put('/{category_id}', response_model=ResponseCategory)
async def update_category(category_id: int, data: CreateCategory, db: Annotated[AsyncSession, Depends(get_db)],
 current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")

    obj = await db.get(Category, category_id)
    if not obj:
        raise HTTPException(404, "Kategoriya topilmadi")

    obj.name = data.name

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db:Annotated[ AsyncSession , Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Category, category_id)
    if not obj:
        raise HTTPException(404, "Kategoriya topilmadi")

    await db.delete(obj)
    await db.commit()
    return


