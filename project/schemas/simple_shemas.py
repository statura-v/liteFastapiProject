from pydantic import BaseModel
# from pydantic import EmailStr

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


class BaseAuthor(BaseModel):
    full_name: str

class AuthorCreate(BaseAuthor):
    pass

class AuthorUpdate(BaseAuthor):
    id: int

class GenreBase(BaseModel):
    # active: bool = True
    name_genre: str

class GenreUpdate(GenreBase):
    id: int

class GenreCreate(GenreBase):
    pass