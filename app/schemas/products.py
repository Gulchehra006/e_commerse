from pydantic import BaseModel, Field,ConfigDict

class CreateProduct(BaseModel):
    name: str
    description: str
    price: int = Field(gt=0, description="Narx musbat son bo'lishi kerak")
    is_stock: bool = True
    category_id: int

class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = Field(default=None, gt=0)
    is_stock: bool | None = None
    category_id: int | None = None

class ResponseProduct(BaseModel):
    id: int
    name: str
    description: str
    price: int
    is_stock: bool
    category_id: int

    model_config = ConfigDict(from_attributes=True)