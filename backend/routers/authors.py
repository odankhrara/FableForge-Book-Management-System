from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/authors", tags=["authors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=schemas.AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        if db.query(models.Author).filter(models.Author.email == payload.email).first():
            raise HTTPException(status_code=409, detail="Email already exists")

        a = models.Author(**payload.dict())
        db.add(a)
        db.commit()
        db.refresh(a)
        return a

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{author_id}", response_model=schemas.AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(models.Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/", response_model=list[schemas.AuthorOut])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(models.Author).offset(skip).limit(limit).all()

@router.put("/{author_id}", response_model=schemas.AuthorOut)
def update_author(author_id: int, payload: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    author = db.get(models.Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    data = payload.dict(exclude_unset=True)
    
    if "email" in data:
        existing = db.query(models.Author).filter(
            models.Author.email == data["email"],
            models.Author.id != author_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")
    
    for key, value in data.items():
        setattr(author, key, value)
    
    db.commit()
    db.refresh(author)
    return author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(models.Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    if author.books:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete author with associated books. Delete books first."
        )
    
    db.delete(author)
    db.commit()