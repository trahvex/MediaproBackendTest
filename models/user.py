from sqlalchemy import Table, Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table("users", meta, Column(
    "id", Integer, primary_key=True), 
    Column("name", String(255)), 
    Column("email", String(255), unique=True))

meta.create_all(engine)

