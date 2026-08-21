from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Page
from app.database.connection import get_db
from app.models.products import Product
from app.schemas.products import CreateProduct, UpdateProduct, ResponseProduct
from app.utils.security import get_current_user

router = APIRouter(tags=['Product'], prefix="/product")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseProduct)
async def add_product(data: CreateProduct, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    try:
        obj = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            is_stock=data.is_stock,
            category_id=data.category_id,
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception as e:
        await db.rollback()  # Xatolik bo'lsa tranzaksiyani bekor qilamiz
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product yaratishda xatolik! Kategoriya ID ({data.category_id}) mavjudligini tekshiring. Xatolik: {str(e)}"
        )


@router.get('/', response_model=Page[ResponseProduct])
async def get_products(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Product)
    return await apaginate(db, query)


@router.put('/{product_id}', response_model=ResponseProduct)
async def update_product(product_id: int, data: UpdateProduct, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Product, product_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)],
current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Sizga ruxsat yo'q")
    obj = await db.get(Product, product_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product topilmadi")

    await db.delete(obj)
    await db.commit()
    return None