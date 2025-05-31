from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from functions.utils import log_event
from models.user import User
from database import get_db
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer, BadSignature
from config import SESSION_SECRET_KEY
import os

router = APIRouter()

#Set up OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/auth/verify-token")
def verify_token(token: str):
    serializer = URLSafeSerializer(SESSION_SECRET_KEY)
    try:
        data = serializer.loads(token)
        return {"valid": True, "data": data}
    except BadSignature:
        return {"valid": False, "error": "Invalid or tampered token"}

@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    # This fetches the user's profile directly from Google
    user_info_response = await oauth.google.get("https://www.googleapis.com/oauth2/v2/userinfo", token=token)
    user_info = user_info_response.json()
    email = user_info.get("email")

    if not email:
        log_event("ERROR", "Login", user_info, "Email not found in Google info.")
        raise HTTPException(status_code=400, detail="Email not found in Google info.")

    user_data = db.query(User).filter(User.email == email).first()

    if not user_data:
        new_user = User(
            name      = user_info.get("given_name"),
            last_name = user_info.get("family_name"),
            username  = user_info.get("given_name")+"-"+user_info.get("family_name"),
            password  = "",
            email     = email,
            company   = "",
            status    = 2
        )

        try:
            #create new user
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_data = new_user
        except Exception as e:
            log_event("ERROR", "User registration", user_info, "there were an error in the database server.")

    # Generate a signed token
    serializer = URLSafeSerializer(SESSION_SECRET_KEY)
    user_token = serializer.dumps({"user_id": user_data.id, "email": user_data.email, "login": "google"})

     # Redirect to frontend with the token (for example: http://localhost:3000/dashboard)
    redirect_url = f"http://localhost:3000/dashboard?token={user_token}"
    return RedirectResponse(url=redirect_url)
    