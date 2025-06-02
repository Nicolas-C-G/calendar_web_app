from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from authlib.integrations.starlette_client import OAuth
from functions.utils import log_event
from models.user import User
from database import get_db
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer, BadSignature
from config import (SESSION_SECRET_KEY, ALLOWED_ORIGINS, GOOGLE_CLIENT_ID, 
                    GOOGLE_CLIENT_SECRET, GOOGLE_SERVER_METADATA_URL, GOOGLE_OAUTH2_USERINFO)
from schemas.auth import TokenData

router = APIRouter()

#Set up OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=GOOGLE_SERVER_METADATA_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.post("/auth/verify-token")
async def verify_token(token_data: TokenData, db: Session = Depends(get_db)):
    try:
        serializer = URLSafeSerializer(SESSION_SECRET_KEY)
        user_data = serializer.loads(token_data.token)
        user_id = user_data.get("user_id")
        user_email = user_data.get("email")

        user = db.query(User).filter_by(id=int(user_id), email=user_email).first
        if not user:
            return {"valid": False, "error": "Invalid or tampered token"}    

        return {"valid": True, "user": user_data}
    except Exception as e:
        return {"valid": False, "error": "Invalid or tampered token"}

@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    user_info_response = await oauth.google.get(GOOGLE_OAUTH2_USERINFO, token=token)
    user_info = user_info_response.json()
    email = user_info.get("email")

    if not email:
        log_event("ERROR", "Login", user_info, "Email not found in Google info.")
        raise HTTPException(status_code=400, detail="Email not found in Google info.")

    user_data = db.query(User).filter(User.email == email).first()

    if not user_data:
        new_user = User(
            name=user_info.get("given_name"),
            last_name=user_info.get("family_name"),
            username=user_info.get("given_name") + "-" + user_info.get("family_name"),
            password="",
            email=email,
            company="",
            status=2
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_data = new_user
        log_event("REGISTER", "User registration", user_info, "The user was successfully created.")

    # Generate signed token
    serializer = URLSafeSerializer(SESSION_SECRET_KEY)
    user_token = serializer.dumps({
        "user_id": user_data.id,
        "email": user_data.email,
        "login": "google"
    })

    log_event("LOGIN", "User login", user_info, "User logged in.")

    # Serve an HTML page that sends the token to React app via postMessage
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Authenticating...</title>
    </head>
    <body>
      <script>
        window.opener.postMessage({{ token: "{user_token}" }}, "{ALLOWED_ORIGINS}");
        window.close();
      </script>
      <p>Logging you in...</p>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)