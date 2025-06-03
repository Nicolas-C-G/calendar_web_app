from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.auth import LoginRequest, RegisterRequest
from models.user import User
from functions.utils import hash_password, verify_password, log_event
from limiter_config import limiter
from database import get_db
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from config import SESSION_SECRET_KEY

router = APIRouter()

serializer = URLSafeSerializer(SESSION_SECRET_KEY)

@router.post("/login")
@limiter.limit("3/minute")
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    
    client_ip = request.client.host

    user = db.query(User).filter(User.username == login_data.username).first()

    if not user:
        log_event("ERROR", "Login", login_data.username+"-"+str(client_ip), "Invalid user")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(login_data.password, user.password):
        log_event("ERROR", "Login", login_data.username+"-"+str(client_ip), "Invalid password")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    log_event("INFO", "Login", user.username+"-"+str(client_ip), "Login successful")

    token_data = {
        "user_id": user.id,
        "email": user.email,
        "login": "normal"
    }
    serializer = URLSafeTimedSerializer(SESSION_SECRET_KEY)
    session_token = serializer.dumps(token_data)

    return {"token": session_token}

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exist")
    
    data = request.dict()
    data["status"] = 1
    data["password"] = hash_password(data["password"])

    try:
        user = User(**data)
        db.add(user)
        db.commit()
    except Exception as e:
        log_event("ERROR", "register", "DB error", str(e))

    return { "message": "User created successfully" }