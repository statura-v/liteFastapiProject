from pydantic import BaseModel
from typing import Optional

class GenreBase(BaseModel):
    # active: bool = True
    name_genre: str


class GenreUpdate(GenreBase):
    id: int


class GenreCreate(GenreBase):
    pass

class IntDate(BaseModel):
    year_first: int
    year_second: int


class LimitStatus(BaseModel):
    limit: int = 1
    offset: int
    status: Optional[bool] = None 