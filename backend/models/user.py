from sqlalchemy import Column, Integer, String
from config import base

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name      = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username  = Column(String(255), unique=True, nullable=False)
    password  = Column(String(255), nullable=False)
    email     = Column(String(255), nullable=False)
    company   = Column(String(255), nullable=False)
    status    = Column(Integer, nullable=False)
