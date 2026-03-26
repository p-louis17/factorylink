from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth, supplier, manufacturer, admin 
from app.models.database import create_tables
from app.models.Models import User

app = FastAPI(
    title="Factory Link"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(supplier.router)
app.include_router(manufacturer.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup():
    create_tables()

@app.on_event("startup")
def startup():
    create_tables()
    # create default admin
    from app.models.database import SessionLocal
    from app.auth_jwt import hash_password
    db = SessionLocal()
    existing = db.query(User).filter(User.email == "admin@factorylink.com").first()
    if not existing:
        admin_user = User(
            name="Admin",
            email="admin@factorylink.com",
            password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
    db.close()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": None})

