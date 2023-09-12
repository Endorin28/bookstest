from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    id: int
    title : str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description , rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequests(BaseModel):
    id: Optional[int] = Field(title='Id not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'coding with roby!',
                'description': 'a new desc of book',
                'rating': 5
            }
        }


BOOKS = [
    Book(1, 'computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPi', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master enpoint', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Autrhor 1', 'Book description', 2),
    Book(5, 'HP2', 'Autrhor 2', 'Book description', 3),
    Book(6, 'HP3', 'Autrhor 3', 'Book description', 1),

]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
@app.post("/create-book")
async def create_book(book_request: BookRequests):
    new_book = Book(**book_request.dict())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
   # if len(BOOKS) > 0:
   #     book.id = BOOKS[-1].id +1
   # else:
   #     book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book