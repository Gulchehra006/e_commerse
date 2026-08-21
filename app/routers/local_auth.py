from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.users import User
from app.schemas.users import TokenResponse, UserRegister
from app.utils.security import hash_password, create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["Local Auth"])


@router.post("/register")
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    existing = result.scalars().first()

    if existing and existing.password:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan")

    user = User(
        email=data.email,
        full_name=data.full_name,
        password=hash_password(data.password),
        auth_provider="LOCAL",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"msg": "Ro'yxatdan muvaffaqqiyatli o'tdingiz"}


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Email yoki parol noto'g'ri")

    if user.password is None:
        raise HTTPException(
            status_code=400,
            detail="Bu akkaunt Google orqali yaratilgan. Google bilan kiring yoki avval parol o'rnating.",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Email yoki parol noto'g'ri")

    return TokenResponse(access_token=create_access_token(user.id, user.email))