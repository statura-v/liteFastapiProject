from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db_session
from schemas.simple_shemas import BookCreate, BookUpdate, BookResponeWithAuthorName, BookWithGenre
from models.crud import create_book, get_book_by_id, delete_book_by_id, update_book
from models.service import search_book_by_title, search_book_by_author, filter_book_by_genre
from typing import List

book_router = APIRouter(prefix="/book", tags=["Books operations"])

@book_router.post("/load", response_model=BookCreate)
def create_book_router(book: BookCreate, db: Session = Depends(get_db_session)) -> BookCreate:
    try:
        current_book = create_book(db, book)
        if not current_book:
            raise HTTPException(status_code=500, detail="Failed to create book")
        return current_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@book_router.get("/{book_id}", response_model=BookUpdate)
def return_book_by_id(book_id: int, db: Session = Depends(get_db_session)):
    try:
        current_book =  get_book_by_id(db, book_id)
        if not current_book:
            raise HTTPException(status_code=404, detail="Not Find the book")
        return current_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@book_router.delete("/{book_id}", response_model=BookCreate)
def del_book_by_id(book_id: int, db: Session= Depends(get_db_session)):
    try:
        current_book = delete_book_by_id(book_id=book_id, database=db)
        if not current_book:
            raise HTTPException(status_code=500, detail="Failed to delete book")
        return current_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@book_router.put("/{book_id}", response_model=BookCreate)
def update_book_by_id(book_id: int, book: BookCreate, db: Session = Depends(get_db_session)):
    try:
        current_book =  update_book(database=db, book_id=book_id, schema=book)
        if not current_book:
            raise HTTPException(status_code=500, detail="Not Find the book")
        return current_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@book_router.get("/search_title/{search}", response_model=List[BookUpdate])
def search_books_by_title(search: str, limit: int = 10, db: Session = Depends(get_db_session)):
    try:
        list_books = search_book_by_title(search, limit, db)
        if not list_books:
               raise HTTPException(status_code=404, detail="Not Find the books")
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@book_router.get('/search_author/{search}', response_model=List[BookResponeWithAuthorName])
def search_book_by_author_name(search: str, limit: int = 10, db: Session = Depends(get_db_session)):
    try:
        list_books = search_book_by_author(search, limit, db)
        if not list_books:
            raise HTTPException(status_code=404, detail="Not find book By author")
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@book_router.get('/search_genre/{search}', response_model=List[BookWithGenre])
def filter_book_by_genre_name(search: str, limit: int = 10, asc: bool = True, db: Session = Depends(get_db_session)):
    try:
        list_books = filter_book_by_genre(search=search, limit=limit, asc_flag=asc, database=db)
        if not list_books:
            raise HTTPException(status_code=404, detail="Not find book By author")
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))