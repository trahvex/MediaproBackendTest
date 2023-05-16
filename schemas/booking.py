from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

class Booking(BaseModel):
    user_id: int
    book_id: int
    booking_date: Optional[str] = Field(str(datetime.today().date()))
    return_date: Optional[str] = Field(str(datetime.today().date()+timedelta(days=28)))