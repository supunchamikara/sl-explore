# SL·Explore

A web application to discover and share Sri Lanka's tourist attractions. Users can browse attractions by province and district, add new places, upload photos, and leave comments.

---

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy (SQLite)
- **Templating:** Jinja2
- **Frontend:** Bootstrap 5 + Bootstrap Icons
- **Auth:** Session-based (itsdangerous) with bcrypt password hashing
- **Package manager:** uv

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) installed

### Setup

```bash
git clone git@github.com:supunchamikara/sl-explore.git
cd sl-explore
bash setup.sh
```

`setup.sh` will:
- Create a `.venv` virtual environment
- Install all dependencies
- Create required directories (`static/uploads/`, `static/css/`)

### Run the app

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Seeding Sample Data

Two seed scripts are included to populate the database with real Sri Lanka attractions.

```bash
# Seed 12 attractions with images
python seed.py

# Seed 52 more attractions across all 9 provinces
python seed_more.py
```

Both scripts create two demo user accounts:
| Email | Password |
|---|---|
| demo@slexplore.com | demo1234 |
| amara@slexplore.com | demo1234 |

---

## Admin Account

A built-in admin account is auto-created when the app starts for the first time.

| Username | Password |
|---|---|
| admin | admin |

### What admins can do

- Access the **Admin Panel** at `/admin` via the navbar
- View all attractions in a paginated table with stats (total attractions, users, comments, photos)
- **Edit** any attraction — update name, description, province/district, GPS coordinates, and manage photos
- **Delete** any attraction (removes DB record + uploaded images from disk)
- Admin badge is shown in the navbar and on attraction detail pages

### Admin login

On the login page, enter `admin` as the username (not an email) and `admin` as the password. After login, you are automatically redirected to the Admin Panel.

---

## Features

- **Browse attractions** with province → district filter and 9-per-page pagination
- **Attraction detail page** with photo gallery, GPS coordinates, Google Maps link, and comments
- **Add attractions** (registered users) with up to 4 photo uploads and GPS auto-detect
- **Comments** on any attraction (registered users only)
- **Responsive design** with an earthy green color palette

---

## Project Structure

```
sl-explore/
├── main.py              # FastAPI app, routes, lifespan
├── models.py            # SQLAlchemy models (User, Attraction, AttractionImage, Comment)
├── database.py          # DB engine, session, base
├── auth.py              # Password hashing and verification (bcrypt)
├── data.py              # Sri Lanka provinces and districts data
├── seed.py              # Seed 12 attractions with images
├── seed_more.py         # Seed 52 more attractions
├── setup.sh             # Environment setup script
├── pyproject.toml       # Project dependencies
├── static/
│   ├── css/style.css    # Custom styles
│   ├── favicon.svg      # Site favicon
│   └── uploads/         # Uploaded attraction images (git-ignored)
└── templates/           # Jinja2 HTML templates
    ├── base.html
    ├── index.html
    ├── attraction_detail.html
    ├── add_attraction.html
    ├── edit_attraction.html
    ├── admin.html
    ├── login.html
    └── register.html
```

---

## Notes

- The SQLite database (`travel.db`) and uploaded images (`static/uploads/`) are git-ignored. They are generated locally when you run the app and seed scripts.
- The admin account is auto-created on first startup — no manual setup needed.
- GPS coordinates can be auto-filled using the browser's Geolocation API when adding or editing an attraction.
