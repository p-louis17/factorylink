from passlib.context import CryptContext
from jose import jwt 
from datetime import timedelta, datetime 
from app.models.database import get_db
from fastapi import Depends, Cookie
from sqlalchemy.orm import Session
from app.models.Models import User
from decouple import config


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
        access_token: str = Cookie(default=None),
        db : Session = Depends(get_db) ) -> User:
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
    user_id = payload.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    return user



