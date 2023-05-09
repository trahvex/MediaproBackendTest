from sqlalchemy import Table, Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

books = Table("books", meta, Column(
    "id", Integer, primary_key=True), 
    Column("title", String(255)), 
    Column("author", String(255)),
    UniqueConstraint("title", "author"))


meta.create_all(engine)

