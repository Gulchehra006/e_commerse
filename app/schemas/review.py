from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ReviewBase(BaseModel):
    text: str
    rate: float = Field(ge=1, le=5)
    product_id: int


class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    text: str
    rate: float= Field(None, ge=1, le=5)

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)