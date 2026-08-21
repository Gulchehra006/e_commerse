import os
from fastapi import APIRouter, Request, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.users import User
from app.utils.security import create_access_token
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["Google OAuth"], prefix="/auth/google")


oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="Google autentifikatsiyasi muvaffaqiyatsiz")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="User ma'lumotlari topilmadi")

    google_id = user_info["sub"]
    email = user_info["email"]
    full_name = user_info.get("name")
    avatar = user_info.get("picture")

    user = db.execute(select(User).where(User.google_id == google_id)).scalars().first()

    if not user:
        user = User(
            email=email,
            full_name=full_name,
            avatar_url=avatar,
            google_id=google_id,
            auth_provider="GOOGLE",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.full_name = full_name
        user.avatar_url = avatar
        db.commit()

    access_token = create_access_token(user.id, user.email)
    return RedirectResponse(
        url=f"http://localhost:5500/?access_token={access_token}"
    )