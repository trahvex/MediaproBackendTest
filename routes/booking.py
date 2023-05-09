import json
from typing import List
from fastapi import APIRouter, Response
from config.db import conn
from models.booking import bookings
from models.book import books
from models.user import users
from schemas.booking import Booking
from datetime import datetime, timedelta
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

booking = APIRouter()

@booking.get('/bookings', response_model=List[Booking], tags=["bookings"])
def get_bookings():
    booking_data = [booking._asdict() for booking in conn.execute(bookings.select()).fetchall()]
    return Response(json.dumps(booking_data, indent=4, sort_keys=True, default=str), HTTP_200_OK)

@booking.get('/bookings/{id}', response_model=Booking, tags=["bookings"])
def get_booking(id: str):
    result =  conn.execute(bookings.select().where(bookings.c.id == id)).first()
    if not result:
        return Response("Booking with id " + id + " not found", HTTP_404_NOT_FOUND)
    return Response(json.dumps(result._asdict(), indent=4, sort_keys=True, default=str), HTTP_200_OK)

@booking.post('/bookings', tags=["bookings"])
def create_booking(booking: Booking):
    book_query = books.select().where(books.c.id == booking.book_id)
    user_query = users.select().where(users.c.id == booking.user_id)
    book = conn.execute(book_query).first()
    user = conn.execute(user_query).first()

    if not book:
        return Response("Book with id " + str(booking.book_id) + " not found", HTTP_404_NOT_FOUND)
    if not user:
        return Response("User with id " + str(booking.user_id) + " not found", HTTP_404_NOT_FOUND)

    booking_date = datetime.strptime(booking.booking_date, '%Y-%m-%d').date() if booking.booking_date else datetime.today().date()
    print(str(booking_date), str(booking_date + timedelta(days=28)))
    return_date = datetime.strptime(booking.return_date, '%Y-%m-%d').date() if booking.return_date else booking.booking_date + timedelta(days=28)

    # Check book is not already booked for booking_date
    existing_booking = conn.execute(bookings.select().where(bookings.c.book_id == booking.book_id).where(bookings.c.return_date > booking_date)).first()
    if existing_booking:
        return Response("Book already booked until " + str(existing_booking.return_date), HTTP_400_BAD_REQUEST)

    new_booking = {"user_id": booking.user_id, "book_id": booking.book_id, "booking_date": booking_date, "return_date": return_date}
    result = conn.execute(bookings.insert().values(new_booking))
    conn.commit()

    return Response("Booked " + book.title + " by " + user.name + " until " + str(return_date), HTTP_200_OK)
    
@booking.put('/bookings/{id}', response_model=Booking, tags=["bookings"])
def update_booking(id: str, booking: Booking):
    result = conn.execute(bookings.select().where(bookings.c.id == id)).first()
    if not result:
        return Response("Booking with id " + id + " not found", HTTP_404_NOT_FOUND)
    conn.execute(bookings.update().values(return_date=booking.return_date).where(bookings.c.id == id))
    result = conn.execute(bookings.select().where(bookings.c.id == id)).first()
    return Response(json.dumps(result._asdict(), indent=4, sort_keys=True, default=str), HTTP_200_OK)
    
@booking.delete('/bookings/{id}', tags=["bookings"])
def delete_booking(id: str):
    conn.execute(bookings.delete().where(bookings.c.id == id))
    conn.commit()
    return Response("Deleted booking with id " + id, HTTP_200_OK)

