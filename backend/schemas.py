from pydantic import BaseModel, EmailStr, Field

# ---------- Authors ----------
class AuthorBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name:  str = Field(min_length=1, max_length=100)
    email: EmailStr

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name:  str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None

class AuthorOut(AuthorBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Books ----------
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    isbn: str = Field(min_length=3, max_length=32)
    publication_year: int | None = None
    available_copies: int = Field(default=1, ge=0)
    author_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    isbn: str | None = Field(default=None, min_length=3, max_length=32)
    publication_year: int | None = None
    available_copies: int | None = Field(default=None, ge=0)
    author_id: int | None = None

class BookOut(BookBase):
    id: int
    class Config:
        from_attributes = True
# --- Chat (LLM) ---
from typing import Optional, List
from pydantic import BaseModel, Field

class ChatIn(BaseModel):
    user_id: int
    message: str = Field(min_length=1)
    conversation_id: Optional[int] = None
    title: Optional[str] = None

class ChatOut(BaseModel):
    conversation_id: int
    reply: str

class ConversationOut(BaseModel):
    id: int
    user_id: int
    title: Optional[str] = None
    class Config:
        from_attributes = True

class ChatMessageOut(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    class Config:
        from_attributes = True

class MessagesOut(BaseModel):
    conversation_id: int
    messages: List[ChatMessageOut]
