from sqlalchemy.orm import Session
from db import get_db_session 
from models.db_models import Book, Author
from schemas.simple_shemas import *

def get_book_by_id(database: Session, book_id: int):
    return database.query(Book).get(book_id)


def create_book(database: Session, schema: BookCreate):
    book = Book(**schema.dict())
    database.add(book)
    database.commit()
    return book


def delete_book_by_id(database: Session, book_id: int):
    book = database.query(Book).get(book_id)
    if not book:
        return book
    database.delete(book)
    database.commit()
    return book


def update_book(database: Session, book_id: int, schema: BookUpdate):
    book = database.query(Book).get(book_id)
    if not book:
        return book
    # this_dict = schema.dict()
    # print(this_dict)
    # for key, value in this_dict:
    #     if hasattr(book, key):
    #         setattr(book, key, value)
    book.title = schema.title
    book.isbn = schema.isbn
    book.year_release = schema.year_release
    database.commit()
    database.refresh(book)

    return book

def create_author(database: Session, schema: AuthorCreate):
    # print(schema.dict())
    # author = Author(schema.dict())
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
    