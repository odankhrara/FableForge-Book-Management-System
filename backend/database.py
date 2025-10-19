from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DB_URL = "mysql+pymysql://app:app_pass@localhost:3307/library_db"  

engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
