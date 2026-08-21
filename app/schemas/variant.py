from pydantic import BaseModel, ConfigDict


class CreateVariant(BaseModel):
    name: str
    product_id: int

class UpdateVariant(BaseModel):
    name: str | None = None
    product_id: int | None = None

class ResponseVariant(BaseModel):
    id: int
    name: str
    product_id: int

    model_config = ConfigDict(from_attributes=True)