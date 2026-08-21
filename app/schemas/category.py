from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str


class UpdateCategory(CreateCategory):
    pass


class ResponseCategory(BaseModel):
    id: int
    name: str
