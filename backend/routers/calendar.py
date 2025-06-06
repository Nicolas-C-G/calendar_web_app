from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from routers.auth_google import oauth
from schemas.auth import TokenData
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from config import SESSION_SECRET_KEY
from database import get_db
from models.user import User
import json

router = APIRouter()

@router.post("/calendar/events")
async def get_calendar_events(token_data: TokenData, db: Session = Depends(get_db)):
    
    try:
        # Validate session token
        serializer = URLSafeTimedSerializer(SESSION_SECRET_KEY)
        user_data = serializer.loads(token_data.token, max_age=3600)
        user_id = int(user_data.get("user_id"))

        # Get user's stored Google token
        user = db.query(User).filter_by(id=user_id).first()
        if not user or not user.token:
            raise HTTPException(status_code=403, detail="Google token not found")
        
        google_tokens = json.loads(user.token)

        # Use stored token to access calendar
        calendar_response = await oauth.google.get(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            token=google_tokens
        )

        return calendar_response.json().get("items", [])
    
    except SignatureExpired:
        raise HTTPException(status_code=401, detail="Token expire")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not fetch calendar events")


