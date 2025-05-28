from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config import session_local
from schemas.auth import LoginRequest, RegisterRequest
from models.user import User
from functions.utils import hash_password, verify_password

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

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": f"Welcome, {user.username}!"}

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exist")
    
    data = request.dict()
    data["status"] = 1
    data["password"] = hash_password(data["password"])

    user = User(**data)
    db.add(user)
    db.commit()

    return { "message": "User created successfully" }