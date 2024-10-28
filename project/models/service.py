from models.db_models import Book, Author, Genre
from sqlalchemy.orm import Session

def search_book_by_title(search: str, database: Session):
   books = database.query(Book).filter(Book.title.like(f'%{search}%'))
   if not books:
       return None
   return books


def search_book_by_author(search: str, database: Session):
    books_data = []
    author = database.query(Author).filter(Author.full_name.like(f'{search}')).all()
    if not author:
        return None
    for x in author:
        books_data.extend(x.books)

    return list(set(books_data)) 
    


def filter_book_by_genre(asc=True): #соритировка включается внутрь фильтрации
    pass


def filter_book_by_author():
    pass


def filter_book_by_year():
    pass


def search_author_by_name():
    pass


def search_genre_by_name():
    pass

