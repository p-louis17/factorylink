from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth, supplier, manufacturer, admin 
from app.models.database import create_tables

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

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": None})