from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config import session_local
from schemas.auth import LoginRequest
from models.user import User

router = APIRouter()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": f"Welcome, {user.username}!"}