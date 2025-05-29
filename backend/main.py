from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import base, engine, ALLOWED_HEADERS, ALLOWED_METHODS, ALLOWED_ORIGINS
from schemas.auth import LoginRequest
from routers import auth
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter_config import limiter

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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