from typing import Optional
from pydantic import BaseModel

class Book(BaseModel):
    id: Optional[int]
    title: str
    author: str
