from pydantic import BaseModel


class CreateMedia(BaseModel):
    image: str
    main: bool = False
    product_id: int


class UpdateMedia(BaseModel):
    image: str
    main: bool


class ResponseMedia(BaseModel):
    id: int
    image: str
    main: bool
    product_id: int

