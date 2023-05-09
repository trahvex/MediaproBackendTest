from fastapi import FastAPI
from routes.book import book
from routes.user import user
from routes.booking import booking

app = FastAPI(
    title="Mediapro backend test API to manage a Barcelona's library",
    openapi_tags=[
        {
            "name": "users",
            "description": "Endpoints related to user management"
        },{
            "name": "books",
            "description": "Endpoints related to books management"
        },{
            "name": "bookings",
            "description": "Endpoints related to bookings management"
        }
    ]
)
app.include_router(user)
app.include_router(book)
app.include_router(booking)

