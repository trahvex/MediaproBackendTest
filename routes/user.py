import json
from typing import List
from fastapi import APIRouter, Response
from config.db import conn
from models.user import users
from schemas.user import User
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

user = APIRouter()

@user.get('/users', response_model=List[User], tags=["users"])
def get_users():
    user_data = [user._asdict() for user in conn.execute(users.select()).fetchall()]
    return Response(json.dumps(user_data), HTTP_200_OK)

@user.get('/users/{id}', response_model=User, tags=["users"])
def get_user(id: str):
    result =  conn.execute(users.select().where(users.c.id == id)).first()
    if not result:
        return Response("User with id " + id + " not found", HTTP_404_NOT_FOUND)
    return Response(json.dumps(result._asdict()), HTTP_200_OK)

@user.post('/users', tags=["users"], description="There cannot be more than one user with the same email address.")
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    try:
        result = conn.execute(users.insert().values(new_user))
        conn.commit()
        return Response("New user added with email " + user.email, HTTP_200_OK)
    except IntegrityError:
        return Response("User with email " + user.email + " already exists", HTTP_400_BAD_REQUEST)
    
@user.put('/users/{id}', response_model=User, tags=["users"])
def update_user(id: str, user: User):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    if not result:
        return Response("User with id " + id + " not found", HTTP_404_NOT_FOUND)
    conn.execute(users.update().values(name=user.name, email=user.email).where(users.c.id == id))
    result = conn.execute(users.select().where(users.c.id == id)).first()
    return Response(json.dumps(result._asdict()), HTTP_200_OK)
    
@user.delete('/users/{id}', tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return Response("Deleted user with id " + id, HTTP_200_OK)

