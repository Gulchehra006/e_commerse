import os
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")


DATABASE_URL = f"mysql+aiomysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


SessionLocal = async_sessionmaker(
    bind=engine
)


async def get_db():
    async with SessionLocal() as db:
        yield db