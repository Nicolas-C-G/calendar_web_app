from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_SERVER_METADATA_URL = os.getenv("GOOGLE_SERVER_METADATA_URL")
GOOGLE_OAUTH2_USERINFO = os.getenv("GOOGLE_OAUTH2_USERINFO")

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