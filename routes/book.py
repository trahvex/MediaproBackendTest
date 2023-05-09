import json
from typing import List, Optional
from fastapi import APIRouter, Response
from config.db import conn
from models.book import books
from schemas.book import Book
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

book = APIRouter()

@book.get('/books', response_model=List[Book], tags=["books"])
def get_books(search: Optional[str] = ""):
    results = conn.execute(books.select().where((books.c.title.like(f"%{search}%")) | (books.c.author.like(f"%{search}%")))).fetchall()
    book_data = [book._asdict() for book in results]
    return Response(json.dumps(book_data), HTTP_200_OK)

@book.get('/books/{id}', response_model=Book, tags=["books"])
def get_book(id: str):
    result =  conn.execute(books.select().where(books.c.id == id)).first()
    if not result:
        return Response("Book with id " + id + " not found", HTTP_404_NOT_FOUND)
    return Response(json.dumps(result._asdict()), HTTP_200_OK)

@book.post('/books', tags=["books"])
def create_book(book: Book):
    new_book = {"title": book.title, "author": book.author}
    try:
        result = conn.execute(books.insert().values(new_book))
        conn.commit()
        return Response("New book added", HTTP_200_OK)
    except IntegrityError:
        return Response("Book with title " + book.title + " and author " + book.author + "already exists", HTTP_400_BAD_REQUEST)
    
@book.put('/books/{id}', response_model=Book, tags=["books"])
def update_book(id: str, book: Book):
    result = conn.execute(books.select().where(books.c.id == id)).first()
    if not result:
        return Response("Book with id " + id + " not found", HTTP_404_NOT_FOUND)
    conn.execute(books.update().values(title=book.title, author=book.author).where(books.c.id == id))
    result = conn.execute(books.select().where(books.c.id == id)).first()
    return Response(json.dumps(result._asdict()), HTTP_200_OK)
    
@book.delete('/books/{id}', tags=["books"])
def delete_book(id: str):
    conn.execute(books.delete().where(books.c.id == id))
    conn.commit()
    return Response("Deleted book with id " + id, HTTP_200_OK)

