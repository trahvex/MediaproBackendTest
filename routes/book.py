import json
from math import ceil
from typing import List, Optional
from fastapi import APIRouter, Response
from config.db import conn
from models.book import books
from schemas.book import Book
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

book = APIRouter()

@book.get('/books', response_model=List[Book], tags=["books"], description="Books are returned by pages of 10 items. " +
          "Search parameter allows to search by title and/or author. " +
          "They can be ordered by id, author or title and the order of the list can also be selected between 'asc' and 'desc'.")
def get_books(search: Optional[str] = "", page: Optional[int] = 1, sort_by: Optional[str] = "id", order: Optional[str] = "asc"):
    
    search_query = books.select().where((books.c.title.like(f"%{search}%")) | (books.c.author.like(f"%{search}%")))
    total_books = conn.execute(search_query).scalar()
    if total_books is None:
        return Response("There are no books registered yet.", HTTP_404_NOT_FOUND)

    total_pages = ceil(total_books/10)

    if page < 1 or page > total_pages:
        return Response("Page must be greater than 0 and less than " + str(total_pages) + " for this query.", HTTP_400_BAD_REQUEST)

    order_clause = books.columns[sort_by]
    if order.lower() == 'desc':
        order_clause = order_clause.desc()

    results = conn.execute(
        search_query
        .order_by(order_clause) 
        .offset((page - 1) * 10)
        .limit(10)
    ).fetchall()
    book_data = [book._asdict() for book in results]
    book_data.append(page)
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

