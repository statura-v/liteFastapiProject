from pydantic import BaseModel

class BaseBook(BaseModel):
    # active: bool = True
    title: str
    isbn: str
    year_release: int
    genre_id: int
    price: float
    count: int


class BookCreate(BaseBook):
    author_ids: list[int]


class BookUpdate(BookCreate):
    id: int


class BookResponeWithAuthorName(BaseBook):
    id: int
    author_name: list[str]


class GetBook(BookUpdate):
    pass


class BookWithGenre(BookResponeWithAuthorName):
    genre_name: str
