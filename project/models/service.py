from models.db_models import Book, Author, Genre
from sqlalchemy.orm import Session
from schemas.book_shemas import BookUpdate, BookCreate, BookResponeWithAuthorName, BookWithGenreAndAuthor
from schemas.author_shemas import AuthorWithBooks, BookForAuthors
from schemas.simple_shemas import IntDate, LimitStatus
from sqlalchemy import func, asc, desc, and_
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List


def return_settings(settings_schema: LimitStatus):
    limit = settings_schema.limit if settings_schema.limit is not None else None
    offset = settings_schema.offset if settings_schema.offset is not None else None
    status = settings_schema.status if settings_schema.status is not None else None
    return limit, offset, status


def return_book_with_author_schema_id(books)->List[BookUpdate]:
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


def return_book_with_author_schema_name(books)->List[BookResponeWithAuthorName]:
    book_res = []
    for book in books:
        # print(book.title)
        authors = [author.full_name for author in book.authors]
        schema_res = BookResponeWithAuthorName(
            title=book.title,
            isbn=book.isbn,
            year_release=book.year_release,
            genre_id=book.genre_id,
            price=book.price,
            count=book.count,
            author_name=authors,
            id=book.id
        )
        
        book_res.append(schema_res)
    # print(book_res)
    return book_res


def search_book_by_title(search: str, settings_schema: LimitStatus, database: Session):
    limit, offset, status = return_settings(settings_schema)
    query = (
        select(Book).options(selectinload(Book.authors)).filter(Book.title.like(f'%{search}%')) #selectinload так как свять m2m
    )
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    if not status:
        query = query.order_by(Book.title.desc())
    else:
        query = query.order_by(Book.title.asc())

    books = database.execute(query).scalars().all()
    if not books:
        return None
    book_res = return_book_with_author_schema_id(books)
    return book_res


def search_book_by_author(search: str, settings_schema: LimitStatus, database: Session):
    limit, offset, status = return_settings(settings_schema)
    query =(
        select(Author).options(selectinload(Author.books)).filter(Author.full_name.like(f'%{search}%'))# selectinload так как связь m2m
    )
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    if not status:
        query = query.order_by(Author.title.desc())
    else:
        query = query.order_by(Author.title.desc())
    authors = database.execute(query).scalars().all()

    if not authors:
        return None
    
    books_res = []
    for x in authors:
        if not x.books:
            continue
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

    books_res.sort(key=lambda x: x.title)

    return books_res 
    

def filter_book_by_genre(search: str, database: Session, settings_schema: LimitStatus)->List[BookWithGenreAndAuthor]: #сортировка включается внутрь фильтрации
    limit, offset, status = return_settings(settings_schema)
    query = (
        select(Genre).options(selectinload(Genre.books)).filter(Genre.name_genre == search)# o2m
    )
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    if not status:
        query = query.order_by(Genre.name_genre.desc())
    else:
        query = query.order_by(Genre.name_genre.asc())
    genres = database.execute(query).scalars().all()
    if not genres:
        return None
    books_res = []
    for genre in genres:
        for book in genre.books:
            authors = [author.full_name for author in book.authors]
            schema_res = BookWithGenreAndAuthor(
                title=book.title,
                isbn=book.isbn,
                year_release=book.year_release,
                genre_id=book.genre_id,
                price=book.price,
                count=book.count,
                author_name=authors,
                id=book.id,
                genre_name=genre.name_genre
            )
            books_res.append(schema_res)

    books_res.sort(key=lambda x: x.title)
    
    return books_res

    
def filter_book_by_author(search: str, database: Session, settings_schema: LimitStatus)->List[AuthorWithBooks]:
    limit, offset, status = return_settings(settings_schema)
    query=(
        select(Author).options(selectinload(Author.books)).filter(Author.full_name == search)
    )
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    query = query.order_by(Author.full_name)
    # if not status:
    #     query = query.order_by(Author.full_name.desc())
    # else:
    #     
    query = query.order_by(Author.full_name.asc())
    authors = database.execute(query).scalars().all()
    
    author_res = []

    if not authors:
        return None
    # sorted_authors = sorted(authors, key=lambda x: x.full_name, reverse=not asc_flag)
    for author in authors:
        book_lst = []
        if not author.books:
            continue
        sorted_lst_books = sorted(author.books, key=lambda x: x.title, reverse= not status)
        for book in sorted_lst_books:
            current_book = BookForAuthors(title=book.title,
                                          isbn=book.isbn,
                                          year_release=book.year_release,
                                          genre_id=book.genre_id,
                                          price=book.price,
                                          count=book.count)
            book_lst.append(current_book)
        current_author = AuthorWithBooks(full_name=author.full_name,
                                         books=book_lst)
        author_res.append(current_author)
    return author_res
    
        
def filter_book_by_year(schema: IntDate, database: Session, settings_schema: LimitStatus)->List[BookResponeWithAuthorName]:
    limit, offset, status =  return_settings(settings_schema)
    query =(
        select(Book).options(selectinload(Book.authors)).limit(limit)
    )
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    conditions = []
    if schema.year_first:
        conditions.append(Book.year_release >= schema.year_first)
    if schema.year_second:
        print(schema.year_second)
        conditions.append(Book.year_release <= schema.year_second)
    if not status:
        query = query.order_by(Book.year_release.desc())
    else:
        query = query.order_by(Book.year_release.desc())
    query = query.where(and_(*conditions))
    

    # compiled_query = query.compile(compile_kwargs={"literal_binds": True})
    # print(compiled_query)

    books = database.execute(query).scalars().all()
    if not books:
        return None
    books_res = return_book_with_author_schema_name(books)
    # books_res = sorted(books_res, key=lambda x: x.title)
    return books_res
    
    
def search_author_by_name(): #Мне лень, так как скучновато
    pass


def search_genre_by_name():
    pass


def return_all_book(schema_settings: LimitStatus, database: Session):
    limit, offset, status = return_settings(schema_settings)
    # print("start 2")
    query=(
        select(Book).options(selectinload(Book.authors)).offset(offset).limit(limit)
    )
    if status:
        query = query.order_by(Book.title.asc())
    else:
        query = query.order_by(Book.title.desc())
    books = database.execute(query).scalars().all()
    # print(books)
    return return_book_with_author_schema_name(books)

