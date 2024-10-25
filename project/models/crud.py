from sqlalchemy.orm import Session
from db import get_db_session 
from models.db_models import Book, Author, Genre
from schemas.simple_shemas import *


def get_book_by_id(database: Session, book_id: int):
    return database.query(Book).get(book_id)


def create_book(database: Session, schema: BookCreate):
    book = Book(schema.title,
                schema.isbn,
                schema.year_release,
                schema.price,
                schema.count,
                schema.genre_id)
    
    genre = database.query(Genre).get(schema.genre_id)
    if not genre:
        return None

    for i in schema.author_ids:
        author = database.query(Author).get(i)
        if not author:
            return None
        book.authors.append(author)
    database.add(book)
    database.commit()
    return book


def delete_book_by_id(database: Session, book_id: int):
    book = database.query(Book).get(book_id)
    if not book:
        return None
    database.delete(book)
    database.commit()
    return book


def update_book(database: Session, book_id: int, schema: BookUpdate):
    book = database.query(Book).get(book_id)
    if not book:
        return None
    
    genre = database.query(Genre).get(schema.genre_id)
    if not genre:
        return None
    
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
            return None
        book.authors.append(author)

    database.commit()
    database.refresh(book)

    return book


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
    