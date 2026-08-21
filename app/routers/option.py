from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.option import Option
from app.schemas.option import CreateOption, UpdateOption, ResponseOption
from app.utils.security import get_current_user

router = APIRouter(tags=['Option'], prefix="/option")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseOption)
async def add_option(data: CreateOption, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    try:
        obj = Option(
            name=data.name,
            image=data.image,
            variant_id=data.variant_id
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Option yaratishda xatolik! kiritilgan variant_id ({data.variant_id}) bazada mavjudligini tekshiring."
        )


@router.get('/', response_model=list[ResponseOption])
async def get_option(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Option))
    return result.scalars().all()


@router.put('/{option_id}', response_model=ResponseOption)
async def update_option(option_id: int, data: UpdateOption, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Option, option_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Option topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete('/{option_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_option(option_id: int, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Option, option_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Option topilmadi")

    await db.delete(obj)
    await db.commit()
    return None