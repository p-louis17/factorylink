from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import RedirectResponse
from app.models.Models import User, Supplier, MaterialListing, MaterialRequest, StatusEnum
from app.auth_jwt import get_current_user
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter(prefix="/supplier", tags=["supplier"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "supplier":
        return RedirectResponse(url="/", status_code=303)

    supplier = db.query(Supplier).filter(Supplier.user_id==current_user.user_id).first()
    listings = db.query(MaterialListing).filter(MaterialListing.supplier_id==supplier.supplier_id).all()

    return templates.TemplateResponse("supplier_dashboard.html", {
        "request": request,
        "user": current_user,
        "supplier": supplier,
        "listings": listings
    })
    
@router.post("/profile")
def update_profile(
    company_name: str = Form(...),
    location: str = Form(...),
    material_types: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    supplier = db.query(Supplier).filter(Supplier.user_id == current_user.user_id).first()

    supplier.company_name = company_name
    supplier.location = location
    supplier.material_types = material_types
    db.commit()
    return RedirectResponse(url="/supplier/dashboard", status_code=303)

@router.post("/create_listing")
def create_listing(
     material_name: str = Form(...),
     quantity: float = Form(...),
     unit: str = Form(...),
     price_per_unit: float = Form(...),
     description: str = Form(...),
     db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user)

):
    supplier = db.query(Supplier).filter(Supplier.user_id == current_user.user_id).first()

    listing = MaterialListing (
        supplier_id=supplier.supplier_id,
        material_name=material_name,
        quantity=quantity,
        unit=unit,
        price_per_unit=price_per_unit,
        description=description
    )
    db.add(listing)
    db.commit()
    return RedirectResponse(url="/supplier/dashboard", status_code=303)

@router.post("/requests/{request_id}/accept")
def accept_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = db.query(MaterialRequest).filter(MaterialRequest.request_id == request_id).first()
    if req:
        req.status = StatusEnum.in_progress
        db.commit()
    return RedirectResponse(url="/supplier/dashboard", status_code=303)

@router.post("/requests/{request_id}/decline")
def decline_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = db.query(MaterialRequest).filter(MaterialRequest.request_id == request_id).first()
    if req:
        req.status = StatusEnum.declined
        db.commit()
    return RedirectResponse(url="/supplier/dashboard", status_code=303)
