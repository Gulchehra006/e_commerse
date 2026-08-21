from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.media import Media
from app.schemas.media import CreateMedia, UpdateMedia, ResponseMedia
from app.utils.security import get_current_user

router = APIRouter(tags=['Media'], prefix="/media")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseMedia)
async def add_media(data: CreateMedia, db: Annotated[AsyncSession, Depends(get_db)],
                    current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    try:
        obj = Media(
            image=data.image,
            main=data.main,
            product_id=data.product_id
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Media yaratishda xatolik! Kiritilgan product_id ({data.product_id}) bazada mavjudligini tekshiring. Xatolik: {str(e)}"
        )


@router.get('/', response_model=list[ResponseMedia])
async def get_media(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Media))
    return result.scalars().all()


@router.put('/{media_id}', response_model=ResponseMedia)
async def update_media(media_id: int, data: UpdateMedia, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Media, media_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete('/{media_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(media_id: int, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Media, media_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media topilmadi")

    await db.delete(obj)
    await db.commit()
    return None