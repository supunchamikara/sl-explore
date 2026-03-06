import json
import uuid
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request, Depends, Form, File, UploadFile, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from database import engine, get_db, Base
from models import User, Attraction, AttractionImage, Comment
from auth import hash_password, verify_password
from data import PROVINCES_DISTRICTS

UPLOAD_DIR = Path("static/uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_IMAGES = 4
PER_PAGE = 9
ADMIN_PER_PAGE = 15


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Add is_admin column if it doesn't exist (safe migration for existing DBs)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
            conn.commit()
        except Exception:
            pass  # column already exists

    # Create admin user if not present
    db = next(get_db())
    try:
        if not db.query(User).filter(User.email == "admin").first():
            admin = User(
                email="admin",
                hashed_password=hash_password("admin"),
                is_admin=True,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

    yield


app = FastAPI(lifespan=lifespan, title="Sri Lanka Tourist Attractions")
app.add_middleware(SessionMiddleware, secret_key="sl-travel-secret-key-change-in-prod")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    user_id = request.session.get("user_id")
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    return None


def require_admin(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {"request": request, "current_user": None}
    )


@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email already registered.", "current_user": None},
        )
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "current_user": None}
    )


@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password.", "current_user": None},
        )
    request.session["user_id"] = user.id
    if user.is_admin:
        return RedirectResponse("/admin", status_code=303)
    return RedirectResponse("/", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    province: Optional[str] = Query(default=None),
    district: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    query = db.query(Attraction)
    if province:
        query = query.filter(Attraction.province == province)
    if district:
        query = query.filter(Attraction.district == district)

    total = query.count()
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = min(page, total_pages)

    attractions = (
        query.order_by(Attraction.created_at.desc())
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
        .all()
    )

    districts_for_province = PROVINCES_DISTRICTS.get(province, []) if province else []
    user = get_current_user(request, db)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "attractions": attractions,
        "current_user": user,
        "provinces": list(PROVINCES_DISTRICTS.keys()),
        "provinces_districts_json": json.dumps(PROVINCES_DISTRICTS),
        "selected_province": province or "",
        "selected_district": district or "",
        "districts_for_province": districts_for_province,
        "page": page,
        "total_pages": total_pages,
        "total": total,
        "per_page": PER_PAGE,
    })


@app.get("/attraction/{attraction_id}", response_class=HTMLResponse)
async def attraction_detail(
    request: Request, attraction_id: int, db: Session = Depends(get_db)
):
    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    user = get_current_user(request, db)
    return templates.TemplateResponse(
        "attraction_detail.html",
        {"request": request, "attraction": attraction, "current_user": user},
    )


# ---------------------------------------------------------------------------
# Authenticated routes
# ---------------------------------------------------------------------------

@app.get("/add", response_class=HTMLResponse)
async def add_attraction_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("add_attraction.html", {
        "request": request,
        "current_user": user,
        "provinces": list(PROVINCES_DISTRICTS.keys()),
        "provinces_districts_json": json.dumps(PROVINCES_DISTRICTS),
    })


@app.post("/add")
async def add_attraction(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    province: str = Form(...),
    district: str = Form(...),
    latitude: Optional[str] = Form(None),
    longitude: Optional[str] = Form(None),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)

    lat = float(latitude) if latitude and latitude.strip() else None
    lng = float(longitude) if longitude and longitude.strip() else None

    attraction = Attraction(
        name=name, description=description,
        province=province, district=district,
        latitude=lat, longitude=lng,
        user_id=user.id,
    )
    db.add(attraction)
    db.flush()

    saved = 0
    for img in images:
        if saved >= MAX_IMAGES:
            break
        if not img.filename or img.filename == "":
            continue
        ext = Path(img.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue
        filename = f"{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(img.file, f)
        db.add(AttractionImage(attraction_id=attraction.id, image_path=f"uploads/{filename}"))
        saved += 1

    db.commit()
    return RedirectResponse(f"/attraction/{attraction.id}", status_code=303)


@app.post("/attraction/{attraction_id}/comment")
async def add_comment(
    request: Request,
    attraction_id: int,
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=404)
    db.add(Comment(attraction_id=attraction_id, user_id=user.id, content=content))
    db.commit()
    return RedirectResponse(f"/attraction/{attraction_id}#comments", status_code=303)


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    province: Optional[str] = Query(default=None),
    district: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=303)

    query = db.query(Attraction)
    if province:
        query = query.filter(Attraction.province == province)
    if district:
        query = query.filter(Attraction.district == district)

    total = query.count()
    total_pages = max(1, (total + ADMIN_PER_PAGE - 1) // ADMIN_PER_PAGE)
    page = min(page, total_pages)

    attractions = (
        query.order_by(Attraction.created_at.desc())
        .offset((page - 1) * ADMIN_PER_PAGE)
        .limit(ADMIN_PER_PAGE)
        .all()
    )

    # Stats
    stats = {
        "total_attractions": db.query(Attraction).count(),
        "total_users": db.query(User).filter(User.is_admin == False).count(),
        "total_comments": db.query(Comment).count(),
        "total_images": db.query(AttractionImage).count(),
    }

    districts_for_province = PROVINCES_DISTRICTS.get(province, []) if province else []

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "current_user": user,
        "attractions": attractions,
        "stats": stats,
        "provinces": list(PROVINCES_DISTRICTS.keys()),
        "provinces_districts_json": json.dumps(PROVINCES_DISTRICTS),
        "selected_province": province or "",
        "selected_district": district or "",
        "districts_for_province": districts_for_province,
        "page": page,
        "total_pages": total_pages,
        "total": total,
        "per_page": ADMIN_PER_PAGE,
    })


@app.get("/attraction/{attraction_id}/edit", response_class=HTMLResponse)
async def edit_attraction_page(
    request: Request, attraction_id: int, db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=303)

    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=404)

    districts_for_province = PROVINCES_DISTRICTS.get(attraction.province, [])

    return templates.TemplateResponse("edit_attraction.html", {
        "request": request,
        "current_user": user,
        "attraction": attraction,
        "provinces": list(PROVINCES_DISTRICTS.keys()),
        "provinces_districts_json": json.dumps(PROVINCES_DISTRICTS),
        "districts_for_province": districts_for_province,
    })


@app.post("/attraction/{attraction_id}/edit")
async def edit_attraction(
    request: Request,
    attraction_id: int,
    name: str = Form(...),
    description: str = Form(...),
    province: str = Form(...),
    district: str = Form(...),
    latitude: Optional[str] = Form(None),
    longitude: Optional[str] = Form(None),
    delete_image_ids: list[int] = Form(default=[]),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=303)

    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=404)

    # Update fields
    attraction.name = name
    attraction.description = description
    attraction.province = province
    attraction.district = district
    attraction.latitude = float(latitude) if latitude and latitude.strip() else None
    attraction.longitude = float(longitude) if longitude and longitude.strip() else None

    # Delete selected images
    for img_id in delete_image_ids:
        img = db.query(AttractionImage).filter(AttractionImage.id == img_id).first()
        if img:
            file_path = Path("static") / img.image_path
            if file_path.exists():
                file_path.unlink()
            db.delete(img)

    # Upload new images (respecting MAX_IMAGES total)
    current_count = db.query(AttractionImage).filter(
        AttractionImage.attraction_id == attraction_id
    ).count()
    slots = MAX_IMAGES - current_count

    for img in images:
        if slots <= 0:
            break
        if not img.filename or img.filename == "":
            continue
        ext = Path(img.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue
        filename = f"{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(img.file, f)
        db.add(AttractionImage(attraction_id=attraction.id, image_path=f"uploads/{filename}"))
        slots -= 1

    db.commit()
    return RedirectResponse("/admin", status_code=303)


@app.post("/attraction/{attraction_id}/delete")
async def delete_attraction(
    request: Request, attraction_id: int, db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=303)

    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=404)

    # Delete image files from disk
    for img in attraction.images:
        file_path = Path("static") / img.image_path
        if file_path.exists():
            file_path.unlink()

    db.delete(attraction)
    db.commit()
    return RedirectResponse("/admin", status_code=303)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

@app.get("/api/districts/{province}")
async def api_districts(province: str):
    return {"districts": PROVINCES_DISTRICTS.get(province, [])}
