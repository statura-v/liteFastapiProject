from models.db_models import Book, Author, Genre
from sqlalchemy.orm import Session
from schemas.simple_shemas import BookUpdate, BookCreate, BookResponeWithAuthorName

def search_book_by_title(search: str, limit: int, database: Session): #Работает
    books = database.query(Book).filter(Book.title.like(f'%{search}%')).limit(limit).all()
    if not books:
        return None
    book_res = []
    
    for book in books:
        authors = [author.id for author in book.authors]
        
        schema_res = BookUpdate(
            title=book.title,
            isbn=book.isbn,
            year_release=book.year_release,
            genre_id=book.genre_id,
            price=book.price,
            count=book.count,
            author_ids=authors,
            id=book.id
        )
        
        book_res.append(schema_res)
    
    return book_res


def search_book_by_author(search: str, limit: int, database: Session):
    books_res = []
    author = database.query(Author).filter(Author.full_name.like(f'%{search}%')).limit(limit).all()
    
    if not author:
        return None
    
    for x in author:
        books = [book for book in x.books]
        for book in books:
            author_name = [author.full_name for author in book.authors]
            schema_res = BookResponeWithAuthorName(title=book.title,
                                    isbn=book.isbn,
                                    year_release=book.year_release,
                                    genre_id=book.genre_id,
                                    price=book.price,
                                    count=book.count,
                                    author_name=author_name,
                                    id=book.id)
            books_res.append(schema_res)

    return books_res 
    


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

