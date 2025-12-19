from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.database import DatabaseService
import os

load_dotenv()

CONNNECTION_STRING = os.getenv("CONNECTION_STRING") or ""
db_service = DatabaseService(CONNNECTION_STRING)

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if db_service.test_connection():
        print("Database connection successful.")
    else:
        print("Database connection failed.")
    db_service.create_tables()
    yield   

app = FastAPI(lifespan=lifespan)    



