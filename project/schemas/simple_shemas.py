from pydantic import BaseModel
from pydantic import EmailStr

class BaseBook(BaseModel):
    title: str
    isbn: str
    year_release: int
    genre_id: int
    price: float
    count: int

class BookCreate(BaseBook):
    pass

class BookUpdate(BaseBook):
    id: int

class GetBook(BookUpdate):
    pass

class BaseAuthor(BaseModel):
    full_name: str

class AuthorCreate(BaseAuthor):
    pass

class AuthorUpdate(BaseAuthor):
    id: int
    