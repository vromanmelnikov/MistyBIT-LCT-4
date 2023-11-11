from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


from src.config import settings

DB_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.POSTGRES_DB}"
engine = create_async_engine(DB_URL, future=True)
AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()
