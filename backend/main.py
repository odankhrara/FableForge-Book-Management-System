from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import authors, books, ai 
from sqlalchemy.exc import IntegrityError

from .database import Base, engine
from .routers import authors, books
from .routers.ai import router as ai_router
from . import models 

app = FastAPI(
    title="Library Management API",
    description="FastAPI + MySQL backend for Authors and Books",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(ai.router) 

@app.get("/")
def root():
    return {"message": "Welcome to Library API. See /docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Nice error messages for DB constraint issues
@app.exception_handler(IntegrityError)
async def integrity_error_handler(_: Request, exc: IntegrityError):
    msg = "Database constraint error."
    raw = str(exc.orig).lower() if exc.orig else ""
    code = status.HTTP_400_BAD_REQUEST
    if "duplicate" in raw or "unique" in raw:
        msg = "Resource violates a unique constraint (e.g., email or ISBN already exists)."
        code = status.HTTP_409_CONFLICT
    elif "foreign key" in raw:
        msg = "Invalid foreign key reference."
        code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(status_code=code, content={"detail": msg})
