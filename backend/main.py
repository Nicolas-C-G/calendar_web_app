from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Dummy user data
USERS = {"nicolas": "1234"}

class LoginRequest(BaseModel):
    username: str
    password: str

#Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],                      # Allow all HTTP methods
    allow_headers=["*"],                      # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Calendar API is running"}

@app.post("/login")
def login(request: LoginRequest):
    if request.username in USERS and USERS[request.username] == request.password:
        return {"message": "Login successful"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")