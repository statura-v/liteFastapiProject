from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime, Text, Boolean, text, Table, Column, Float, DECIMAL
from typing import Annotated, List
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID

class BaseTable(DeclarativeBase):
    created_at = mapped_column(DateTime)
    active: Mapped[bool] = mapped_column(Boolean)


book_authors = Table("book_authors", BaseTable.metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("author_id", Integer, ForeignKey("author.id")),
                    Column("book_id", Integer, ForeignKey("book.id"))
                     )

class User(BaseTable):
    __tablename__ = "user"

    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    addres: Mapped[str] = mapped_column(String(128), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    user_name: Mapped[str] = mapped_column(String(20), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(40), nullable=False)
    number_telephone: Mapped[str] = mapped_column(String(20), nullable=False)



class Book(BaseTable):
    __tablename__ = "book"
    
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256))
    isbn: Mapped[str] = mapped_column(String(128))
    year_release: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey("genre.id"))
    price: Mapped[float] = mapped_column(DECIMAL(2), nullable=True)
    count: Mapped[int] = mapped_column(Integer, nullable=True)  

    authors: Mapped[List["Author"]] = relationship("Author", secondary=book_authors, back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")

    

class Author(BaseTable):
    __tablename__ = "author"
    
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(256))

    books: Mapped[List["Book"]] = relationship("Book", secondary=book_authors, back_populates="authors")


class Genre(BaseTable):
    __tablename__ = "genre"

    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_genre: Mapped[str] = mapped_column(String(128), nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="genre")

