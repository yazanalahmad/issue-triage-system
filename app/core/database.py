from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings



class base(DeclarativeBase):
    pass

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"options": f"-c search_path={settings.db_schema}"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()