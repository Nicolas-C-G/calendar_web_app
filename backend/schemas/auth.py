from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    last_name: str
    username: str
    password: str
    email: str
    company: str