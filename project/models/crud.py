from sqlalchemy.orm import Session
from db import get_db_session 
from models.db_models import Book, Author, Genre
from schemas.book_shemas import BookCreate, BookUpdate
from schemas.author_shemas import AuthorCreate, AuthorUpdate
from schemas.simple_shemas import GenreCreate
from sqlalchemy import func, asc, desc, and_
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from models.service import return_book_with_author_schema_id

def create_dict(**kwargs):
    return kwargs


def get_book_by_id(database: Session, book_id: int):
    query=(
        select(Book).filter(Book.id == book_id)
    )
    book = database.execute(query).scalars().all()
    schema_res =  return_book_with_author_schema_id(book)
    return schema_res[0] #так как одна книга


def create_book(database: Session, schema: BookCreate):
    author_ids_lst = []
    book = Book()

    book.title = schema.title
    book.isbn = schema.isbn            
    book.year_release = schema.year_release            
    book.count = schema.count 
    book.price = schema.price           
           

    genre = database.query(Genre).get(schema.genre_id)
    if not genre:
        return None

    book.genre_id = schema.genre_id  

    for i in schema.author_ids:
        author = database.query(Author).get(i)
        if not author:
            return None
        book.authors.append(author)
        author_ids_lst.append(i)

    book_data = create_dict(
        title=book.title,
        isbn=book.isbn,
        year_release=book.year_release,
        count=book.count,
        price=book.price,
        genre_id=book.genre_id,
        author_ids=author_ids_lst
    )
    
    database.add(book)
    database.commit()
    return book_data


def delete_book_by_id(database: Session, book_id: int):
    author_ids = []
    book = database.query(Book).get(book_id)
    if not book:
        return None

    for author in book.authors:
        if author:
            author_ids.append(author.id)

    book_data = create_dict(
        title=book.title,
        isbn=book.isbn,
        year_release=book.year_release,
        count=book.count,
        price=book.price,
        genre_id=book.genre_id,
        author_ids=author_ids
    )
    database.delete(book)
    database.commit()
    return book_data


def update_book(database: Session, book_id: int, schema: BookUpdate):
    author_ids = []
    book = database.query(Book).get(book_id)
    if not book:
        return None
    print(book)
    
    genre = database.query(Genre).get(schema.genre_id)
    if not genre:
        return None
    print(genre)
    
    book.title = schema.title
    book.isbn = schema.isbn
    book.year_release = schema.year_release
    book.price = schema.price
    book.count = schema.count
    book.genre_id = schema.genre_id
    book.authors.clear()

    for i in schema.author_ids:
        author = database.query(Author).get(i)
        if not author:
            continue
        book.authors.append(author)
        author_ids.append(author.id)
    
    book_data = create_dict(
        title=book.title,
        isbn=book.isbn,
        year_release=book.year_release,
        count=book.count,
        price=book.price,
        genre_id=book.genre_id,
        author_ids=author_ids
    )
    database.commit()
    database.refresh(book)

    return book_data


def create_author(database: Session, schema: AuthorCreate):
    author = Author()
    author.full_name = schema.full_name
    database.add(author)
    database.commit()
    return author


def delete_author_by_id(author_id: int, database: Session):
    author = database.query(Author).get(author_id)
    print(author)
    if not author:
        return author
    database.delete(author)
    database.commit()
    return author


def create_genre(database: Session, schema: GenreCreate):
    genre = Genre()
    genre.name_genre = schema.name_genre
    database.add(genre)
    database.commit()
    return genre
    