# Mediapro Backend Test
This project allows the management of a library via its users, bookings, and books. It is built using the FastAPI web framework and SQLAlchemy for database management.

## Installation

Clone the repository:

```bash
git clone https://github.com/trahvex/MediaproBackendTest
```

Navigate to the project directory:

```bash
cd MediaproBackendTest
```
Install the required packages:

```bash
pip install -r requirements.txt
```
## Usage

Start the FastAPI app using the following command:

```bash
uvicorn app:app --reload
```
Open your browser and go to http://localhost:8000/docs to access the Swagger UI for the API.

Use the API endpoints to manage users, bookings, and books in the library.

## API Endpoints

The following API endpoints are available:
### Users

    - GET /users: Get all users
    - GET /users/{user_id}: Get user by ID
    - POST /users: Create a new user
    - PUT /users/{user_id}: Update user by ID
    - DELETE /users/{user_id}: Delete user by ID

### Books

    - GET /books: Get all books or search by name or author by adding the parameter _search_ to the url
    - GET /books/{book_id}: Get book by ID
    - POST /books: Create a new book
    - PUT /books/{book_id}: Update book by ID
    - DELETE /books/{book_id}: Delete book by ID

### Bookings

    - GET /bookings: Get all bookings
    - GET /bookings/{booking_id}: Get booking by ID
    - POST /bookings: Create a new booking
    - PUT /bookings/{booking_id}: Update booking by ID
    - DELETE /bookings/{booking_id}: Delete booking by ID