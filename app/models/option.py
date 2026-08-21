from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] =  mapped_column(String(50), nullable=False)
    image: Mapped[str] =  mapped_column(String(255), nullable=False)
    variant_id: Mapped[int] = mapped_column(Integer, ForeignKey("variants.id"), nullable=False)
