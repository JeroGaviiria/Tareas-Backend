from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
database_url = "sqlite:///./database.sqlite"

engine = create_engine(database_url,
                       native_datetime=True,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine,
                            autocommit=False,
                            autoflush=False)
Base = declarative_base()
