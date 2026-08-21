from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.products import Product
from app.models.review import Review
from app.schemas.review import ReviewResponse, ReviewCreate, ReviewUpdate
from app.utils.security import get_current_user

router = APIRouter(tags=['Review'], prefix="/review")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ReviewResponse)
async def add_review(
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Asinxron ravishda mahsulot borligini tekshirish
    product = await db.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    obj = Review(
        text=data.text,
        rate=data.rate,
        user_id=current_user.id,
        product_id=data.product_id
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get('/{product_id}', response_model=List[ReviewResponse])
async def get_reviews(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.product_id == product_id))
    return result.scalars().all()


@router.put('/{review_id}', response_model=ReviewResponse)
async def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: AsyncSession = Depends(get_db)
):
    review = await db.get(Review, review_id)

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if data.text is not None:
        review.text = data.text
    if data.rate is not None:
        review.rate = data.rate

    await db.commit()
    await db.refresh(review)

    return review


@router.delete('/{review_id}')
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review = await db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    await db.delete(review)
    await db.commit()

    return {"message": "Deleted successfully"}