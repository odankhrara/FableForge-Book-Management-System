from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.BookOut])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(models.Book).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    if db.query(models.Book).filter_by(isbn=payload.isbn).first():
        raise HTTPException(409, "ISBN already exists")
    if not db.get(models.Author, payload.author_id):
        raise HTTPException(400, "author_id does not reference a valid author")
    b = models.Book(**payload.dict())
    db.add(b); db.commit(); db.refresh(b)
    return b

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    b = db.get(models.Book, book_id)
    if not b:
        raise HTTPException(404, "Book not found")
    return b

@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)):
    b = db.get(models.Book, book_id)
    if not b:
        raise HTTPException(404, "Book not found")

    data = payload.dict(exclude_unset=True)
    if "isbn" in data:
        exists = db.query(models.Book).filter(models.Book.isbn == data["isbn"], models.Book.id != book_id).first()
        if exists:
            raise HTTPException(409, "ISBN already exists")
    if "author_id" in data and data["author_id"] is not None:
        if not db.get(models.Author, data["author_id"]):
            raise HTTPException(400, "author_id does not reference a valid author")

    for k, v in data.items():
        setattr(b, k, v)
    db.commit(); db.refresh(b)
    return b

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    b = db.get(models.Book, book_id)
    if not b:
        raise HTTPException(404, "Book not found")
    db.delete(b); db.commit()

@router.get("/by-author/{author_id}", response_model=list[schemas.BookOut])
def books_by_author(author_id: int, db: Session = Depends(get_db)):
    if not db.get(models.Author, author_id):
        raise HTTPException(404, "Author not found")
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()
