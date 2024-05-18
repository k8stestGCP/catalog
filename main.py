# main.py

from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from schemas import Book, BookCreate
from crud import get_books, create_book, get_book_by_id
from pubsub import request_verification, subscribe_to_topic
from rentProvider import subscribe_to_topic_rent
from database import get_db
from dependencies import verify_token

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()
    await subscribe_to_topic_rent()

@app.post("/books/", response_model=Book)
async def create_new_book(book: BookCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    try:
        print("Creating book")
        return create_book(db=db, book=book)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book creation failed"
        )

@app.get("/books/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user=Depends(verify_token)):
    books = get_books(db=db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    db_book = get_book_by_id(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
