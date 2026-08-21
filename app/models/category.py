from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

