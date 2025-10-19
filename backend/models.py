from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name  = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), 
                        onupdate=datetime.now)  

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    isbn  = Column(String(32), unique=True, index=True, nullable=False)
    publication_year = Column(Integer)
    available_copies = Column(Integer, nullable=False, server_default=text("1"))
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="RESTRICT"), nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=datetime.now) 

    author = relationship("Author", back_populates="books")



    # --- Chat models for Section 4 ---
from sqlalchemy import Text

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=text("CURRENT_TIMESTAMP"))

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(16), nullable=False)   # "user" | "assistant" | "system"
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    conversation = relationship("Conversation", back_populates="messages")
