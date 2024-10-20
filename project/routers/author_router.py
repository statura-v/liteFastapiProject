from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db_session
from schemas.simple_shemas import AuthorCreate, AuthorUpdate
from models.crud import *

author_router = APIRouter(prefix="/author", tags=["Author operations"])

@author_router.post("/load", response_model=AuthorCreate)
def create_author_router(author: AuthorCreate, db: Session = Depends(get_db_session)):
    try:
        current_author = create_author(database=db, schema=author)
        if not current_author:
            raise HTTPException(status_code=500, detail="Failed to create Author")
        return current_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@author_router.delete("/{author_id}", response_model=AuthorUpdate)
def delete_author_router(author_id: int, db: Session = Depends(get_db_session)):
    try:
        current_author = delete_author_by_id(database=db, author_id=author_id)
        if not current_author:
            raise HTTPException(status_code=500, detail="Failed to delete Author")
        return current_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))