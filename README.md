# FactoryLink

FactoryLink is a web-based marketplace that connects raw material suppliers with local manufacturers across Africa. Suppliers list available materials, manufacturers submit requests, and the platform automatically matches them — reducing import dependency and enabling local industrial growth.

**Live Demo:** https://factorylink.onrender.com

---

## The Problem

African countries export abundant raw materials in unprocessed form while importing finished goods at significantly higher costs. This limits local value addition, job creation, and industrial development. FactoryLink addresses the coordination gap between suppliers and manufacturers by providing a centralized digital platform.

---

## Features

- Supplier registration, profile management, and material listings
- Manufacturer registration, profile management, and material requests
- Automatic matching algorithm — connects requests to available listings by material name and quantity
- Supplier can accept or decline matched requests
- Admin dashboard to monitor all users, listings, and requests
- JWT-based authentication with role-based access control

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (hosted on Neon — no local database setup required)
- **ORM:** SQLAlchemy
- **Auth:** JWT tokens via python-jose, password hashing via passlib/bcrypt
- **Templates:** Jinja2
- **Deployment:** Render

---

## Prerequisites

Only one thing needed:

- **Python 3.12 or higher** — download from https://www.python.org/downloads/

> **Windows users:** During installation, make sure to check **"Add Python to PATH"**

---

## Setup — One Command

The database is already hosted in the cloud. You do not need to install or configure anything else.

### Linux / Mac

```bash
git clone https://github.com/p-louis17/factorylink.git
cd factorylink
chmod +x setup.sh
./setup.sh
```

### Windows

```bash
git clone https://github.com/p-louis17/factorylink.git
cd factorylink
```

Then double-click **`setup.bat`** or run in terminal:

```bash
setup.bat
```

The script will:
- Create a virtual environment
- Install all dependencies
- Create the `.env` file with all required values pre-filled

---

## Running the App

After setup completes:

### Linux / Mac
```bash
source myvenv/bin/activate
uvicorn main:app --reload
```

### Windows
```bash
myvenv\Scripts\activate
uvicorn main:app --reload
```

Then open your browser and go to: **http://localhost:8000**

---

## Default Admin Account

An admin account is created automatically on first startup:

| Email | Password |
|---|---|
| admin@factorylink.com | admin123 |

---

## How It Works

1. A **Supplier** registers, creates a profile, and lists available raw materials with quantity and price
2. A **Manufacturer** registers, creates a factory profile, and submits a material request
3. The system automatically searches for matching supplier listings by material name and quantity
4. If a match is found, the request status changes to **matched** and the supplier is notified
5. The **Supplier** accepts or declines the request from their dashboard
6. The **Manufacturer** sees the updated status in real time
7. An **Admin** can monitor all activity and manage users and listings

---

## Project Structure

```
factorylink/
├── main.py                    # App entry point
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version for Render
├── setup.sh                   # One-command setup for Linux/Mac
├── setup.bat                  # One-command setup for Windows
├── .env.example               # Environment variable template
├── .gitignore
└── app/
    ├── auth_jwt.py            # JWT auth and password hashing
    ├── database.py            # Database connection and session
    ├── models/
    │   └── Models.py          # SQLAlchemy models
    ├── routers/
    │   ├── auth.py            # /auth/register, /auth/login, /auth/logout
    │   ├── supplier.py        # /supplier/dashboard, listings, accept/decline
    │   ├── manufacturer.py    # /manufacturer/dashboard, requests, matching
    │   └── admin.py           # /admin/dashboard
    ├── templates/             # Jinja2 HTML templates
    └── static/css/            # Stylesheet
```

---

## API Documentation

FastAPI generates interactive API documentation automatically. Once the app is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## SRS Document

https://docs.google.com/document/d/1HvT-Qnbrezmt5B3X4LX28emdEPnLx9EY0d6rn90W7c0/edit?tab=t.0#heading=h.gjdgxs
