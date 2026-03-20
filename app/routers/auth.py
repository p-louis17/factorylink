from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from app.models.database import get_db
from datetime import datetime
from app.models.Models import User, RoleEnum
from app.auth_jwt import verify_password, hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(
    name: str = Form (...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form (...),
    db: Session = Depends(get_db)
):
    exisiting_email = db.query(User).filter(User.email==email).first()

    if exisiting_email:
        raise HTTPException(status_code=400, detail="Email already existis")
    
    user = User (
        name=name,
        email=email,
        password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()

    token = create_access_token({"sub": user.user_id, "role": user.role})

    response = RedirectResponse(f"/{role}/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True, max_age=86400)
    return response
    
@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    token = create_access_token({"sub": User.user_id, "role": User.role})

    if password == verify_password(User.password):
       token = create_access_token({"sub": User.user_id, "role": User.role})
       response = RedirectResponse(f"/{User.role}/dashboard", status_code=303)
       response.set_cookie("access_token", token, httponly=True, max_age=86400)
       return response