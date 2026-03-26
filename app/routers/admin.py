from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.auth_jwt import get_current_user
from app.models.Models import User, MaterialListing, MaterialRequest, Notification

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        return RedirectResponse(url="/", status_code=303)
    users = db.query(User).all()
    listings = db.query(MaterialListing).all()
    requests = db.query(MaterialRequest).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request, "user": current_user,
        "users": users, "listings": listings, "requests": requests
    })

@router.post("/users/{user_id}/delete")
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        return RedirectResponse(url="/", status_code=303)
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@router.post("/listings/{listing_id}/remove")
def remove_listing(listing_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        return RedirectResponse(url="/", status_code=303)
    listing = db.query(MaterialListing).filter(MaterialListing.listing_id == listing_id).first()
    if listing:
        db.delete(listing)
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)