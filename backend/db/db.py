from utils.settings import config

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
    
Base = declarative_base()

#Database connection
DATABASE_URL =  f"postgresql+asyncpg://{config.database_username}:{config.database_password}@{config.database_host}:{config.database_port}/{config.database_name}"
# DATABASE_URL = "postgresql+asyncpg://postgres:leooffice@localhost:5432/ticketingsystem"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

#Establish the connection and sync the models to add database tables to the sytem
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

#Create session variable 
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
