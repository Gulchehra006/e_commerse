from pydantic import BaseModel


class CreateOption(BaseModel):
    name: str
    image: str
    variant_id: int


class UpdateOption(BaseModel):
    name: str
    image: str
    variant_id: int



class ResponseOption(BaseModel):
    id: int
    name: str
    image: str
    variant_id: int

