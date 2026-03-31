from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./frete.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 1. Cole a sua URL do Neon/Supabase aqui
# Exemplo: SQLALCHEMY_DATABASE_URL = "postgresql://victor:senha123@ep-mud-surf-123.us-east-2.aws.neon.tech/neondb?sslmode=require"
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_OSlpH0Q5uwmz@ep-damp-forest-amdpvl9q-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 2. O engine do Postgres não precisa do 'connect_args={"check_same_thread": False}'
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
