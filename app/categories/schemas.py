from pydantic import BaseModel
from typing import Literal


class CategoryCreate(BaseModel):
    name: str
    type: Literal["income", "expense"]


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str

    model_config = {"from_attributes": True}