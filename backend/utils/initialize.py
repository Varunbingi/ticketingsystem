from fastapi import FastAPI
from db.db import create_tables
from contextlib import asynccontextmanager
from db import models 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
