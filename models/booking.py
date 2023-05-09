from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Date
from config.db import meta, engine

bookings = Table("bookings", meta,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("booking_date", Date),
    Column("return_date", Date),
)

meta.create_all(engine)