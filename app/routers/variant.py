from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.variant import Variant
from app.schemas.variant import CreateVariant, UpdateVariant, ResponseVariant
from app.utils.security import get_current_user

router = APIRouter(tags=['Variant'], prefix="/variant")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseVariant)
async def add_variant(data: CreateVariant, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    try:
        obj = Variant(
            name=data.name,
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
            detail=f"Variant yaratishda xatolik! product_id ({data.product_id}) bazada borligini tekshiring."
        )


@router.get('/', response_model=list[ResponseVariant])
async def get_variant(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Variant))
    return result.scalars().all()


@router.put('/{variant_id}', response_model=ResponseVariant)
async def update_variant(variant_id: int, data: UpdateVariant, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Variant, variant_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete('/{variant_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(variant_id: int, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Variant, variant_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant topilmadi")

    await db.delete(obj)
    await db.commit()
    return None