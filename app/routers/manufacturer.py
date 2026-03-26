from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import RedirectResponse
from app.models.Models import User, Supplier, MaterialListing, MaterialRequest,Notification, StatusEnum, Manufacturer
from app.auth_jwt import get_current_user
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter(prefix="/manufacturer", tags=["manufacturer"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    if current_user.role != "manufacturer":
        return RedirectResponse(url="/", status_code=303)
    
    manufacturer = db.query(Manufacturer).filter(Manufacturer.user_id==current_user.user_id).first()
    requests = db.query(MaterialRequest).filter(MaterialRequest.manufacturer_id==manufacturer.manufacturer_id).all()
    listings = db.query(MaterialListing).all()

    return templates.TemplateResponse("manufacturer_dashboard.html", {
        "request": request,
        "user": current_user,
        "manufacturer": manufacturer, 
        "requests": requests,
        "listings": listings
    })

@router.post("/profile")
def update_profile(
    factory_name: str = Form(...),
    industry: str = Form(...),
    production_capacity: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.user_id == current_user.user_id).first()
    
    manufacturer.factory_name=factory_name
    manufacturer.industry=industry
    manufacturer.production_capacity=production_capacity
    manufacturer.location=location

    db.commit()

    return RedirectResponse(url="/manufacturer/dashboard", status_code=303)

def run_matching(request_obj: MaterialRequest, db: Session):
    matches = db.query(MaterialListing).filter(
        MaterialListing.material_name.ilike(f"%{request_obj.material_name}%"),
        MaterialListing.quantity >= request_obj.quantity
    ).all()

    if matches:
        best = matches[0]
        request_obj.listing_id = best.listing_id
        request_obj.status = StatusEnum.matched
        
        notif = Notification(
            recipient_id=best.supplier.user_id,
            request_id=request_obj.request_id,
            message=f"New request matched to your listing: {best.material_name}"
        )
        db.add(notif)
    else:
        request_obj.status = StatusEnum.pending

@router.post("/requests/submit")
def submit_request(
    material_name: str = Form(...),
    quantity: float = Form(...),
    unit: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.user_id==current_user.user_id).first()

    request = MaterialRequest(
        manufacturer_id = manufacturer.manufacturer_id,
        material_name=material_name,
        quantity=quantity,
        unit=unit

    )
    db.add(request)
    db.flush()
    run_matching(request, db)
    db.commit()

    return RedirectResponse(url="/manufacturer/dashboard", status_code=303)

