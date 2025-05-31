from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

LOG_FOLDER_PATH = os.getenv("LOG_FOLDER_PATH")

DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

# CORS settings
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
ALLOWED_METHODS = ["*"]
ALLOWED_HEADERS = ["*"]

# SQLAlchemy setup
DB_URI = os.getenv("MYSQL_URI")
engine = create_engine(DB_URI, echo=DEV_MODE)
session_local= sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all ORM models
base = declarative_base()