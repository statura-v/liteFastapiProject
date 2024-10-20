from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime, Text, Boolean, text, Table, Column, Float
from typing import Annotated, List
from datetime import datetime

class BaseConfige(DeclarativeBase):
    created_at = mapped_column(DateTime)
    updated_at = mapped_column(DateTime)


book_authors = Table("book_authors", BaseConfige.metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("author_id", Integer, ForeignKey("author.id")),
                    Column("book_id", Integer, ForeignKey("book.id"))
                     )

class Book(BaseConfige):
    __tablename__ = "book"
    
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256))
    isbn: Mapped[str] = mapped_column(String(128))
    year_release: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey("genre.id"))

    authors: Mapped[List["Author"]] = relationship("Author", secondary=book_authors, back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")

    

class Author(BaseConfige):
    __tablename__ = "author"
    
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(256))

    books: Mapped[List["Book"]] = relationship("Book", secondary=book_authors, back_populates="authors")


class Genre(BaseConfige):
    __tablename__ = "genre"

    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_genre: Mapped[str] = mapped_column(String(128), nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="genre")

