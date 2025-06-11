from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import base, engine, ALLOWED_HEADERS, ALLOWED_METHODS, ALLOWED_ORIGINS
from schemas.auth import LoginRequest
from routers import auth, auth_google, calendar
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter_config import limiter
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# This line to support session-based login (e.g. Google OAuth)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-key"))


# Create tables (only once at startup)
base.metadata.create_all(bind=engine)

#Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # React frontend URL
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,                      # Allow all HTTP methods
    allow_headers=ALLOWED_HEADERS,                      # Allow all headers
)

app.include_router(auth.router)
app.include_router(auth_google.router)
app.include_router(calendar.router)