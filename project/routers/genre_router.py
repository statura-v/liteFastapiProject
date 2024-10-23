from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db_session
from schemas.simple_shemas import GenreUpdate, GenreCreate
from models.crud import create_genre
from typing import List

genre_router = APIRouter(prefix="/genre", tags=["Work with genre"])

@genre_router.post("/load", response_model=GenreCreate)
def create_genre_router(genre: GenreCreate , db: Session = Depends(get_db_session)):
    try:
        genre = create_genre(db, schema=genre)
        if not genre:
            raise HTTPException(status_code=500, detail="Failed to create genre")
        return genre
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))