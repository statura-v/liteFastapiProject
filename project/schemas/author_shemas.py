from pydantic import BaseModel
from typing import List
from schemas.book_shemas import BaseBook


class BookForAuthors(BaseBook):
    pass


class BaseAuthor(BaseModel):
    full_name: str


class AuthorCreate(BaseAuthor):
    pass


class AuthorUpdate(BaseAuthor):
    id: int


class AuthorWithBooks(BaseAuthor):
    books: List[BookForAuthors]