# 🏥 Hospital Management REST API

A production-ready Hospital Management REST API built with Django REST Framework, featuring JWT Authentication, Role-Based Access Control (RBAC), Redis caching, Swagger documentation, and Docker support.

---

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [User Roles & Permissions](#user-roles--permissions)
- [API Documentation](#api-documentation)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Django 4.x + Django REST Framework |
| Database | PostgreSQL 15 |
| Cache / Throttle | Redis 7 |
| Auth | SimpleJWT |
| Docs | drf-spectacular (Swagger + ReDoc) |
| Server | Gunicorn |
| Container | Docker + Docker Compose |

---

## ✨ Features

- JWT Authentication (register, login, logout, token refresh)
- Role-Based Access Control with 4 user roles
- Full CRUD for Doctors, Patients, and Appointments
- Filtering, searching, and ordering on list endpoints
- Pagination (10 results per page)
- Redis caching on frequently accessed endpoints
- API throttling (rate limiting per user and anonymous)
- Swagger UI + ReDoc documentation
- Dockerized with PostgreSQL and Redis
- Settings split into base / local / production

---

## 📁 Project Structure

```
hospital_api/
├── core/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py          # Custom User model with role field
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py     # 8 custom permission classes
├── doctors/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── patients/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── appointments/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── manage.py
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 15
- Redis 7
- pip

### 1. Clone the repository

```bash
git clone https://github.com/mokshatummaluru/hospital_api.git
cd hospital_api
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

```bash
psql postgres
CREATE DATABASE hospital_db;
\q
```

### 5. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create superuser

```bash
python manage.py createsuperuser
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=hospital_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/1
```

---

## 🚀 Running the Project

```bash
# Start Redis
brew services start redis   # Mac
# or
sudo service redis start    # Linux

# Start server
python manage.py runserver
```

Server runs at `http://127.0.0.1:8000`

---

## 🐳 Running with Docker

```bash
# Build and start all containers
docker-compose up -d --build

# Check container status
docker-compose ps

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop containers
docker-compose down
```

Containers started:
- `hospital_web` — Django app on port 8000
- `hospital_db` — PostgreSQL on port 5433
- `hospital_redis` — Redis on port 6380

---

## 📡 API Endpoints

### Auth — `/api/v1/auth/`

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| POST | `/register/` | Register new user | Public |
| POST | `/login/` | Login and get tokens | Public |
| POST | `/logout/` | Blacklist refresh token | Authenticated |
| POST | `/token/refresh/` | Get new access token | Authenticated |
| GET/PATCH | `/profile/` | View or update own profile | Authenticated |

### Doctors — `/api/v1/doctors/`

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | `/` | List all doctors | Authenticated |
| GET | `/<id>/` | Get doctor detail | Authenticated |
| POST | `/create/` | Create doctor profile | Doctor only |
| GET/PATCH | `/my-profile/` | View or update own profile | Doctor / Admin |
| DELETE | `/<id>/delete/` | Delete doctor profile | Admin only |

### Patients — `/api/v1/patients/`

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | `/` | List all patients | Admin / Doctor |
| GET | `/<id>/` | Get patient detail | Admin / Doctor |
| POST | `/create/` | Create patient profile | Patient only |
| GET/PATCH | `/my-profile/` | View or update own profile | Patient only |
| DELETE | `/<id>/delete/` | Delete patient profile | Admin only |

### Appointments — `/api/v1/appointments/`

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | `/` | List all appointments | Admin / Receptionist |
| POST | `/create/` | Book appointment | Authenticated |
| GET | `/<id>/` | Get appointment detail | Admin / Doctor / Receptionist |
| PATCH | `/<id>/update/` | Update appointment | Admin / Doctor |
| POST | `/<id>/cancel/` | Cancel appointment | Authenticated |
| GET | `/my-appointments/` | View own appointments | Authenticated |

---

## 🔑 Authentication

This API uses JWT (JSON Web Tokens).

### Register and get tokens

```bash
POST /api/v1/auth/register/
{
    "username": "doctor1",
    "email": "doctor1@hospital.com",
    "password": "Test@1234",
    "password2": "Test@1234",
    "first_name": "John",
    "last_name": "Smith",
    "role": "DOCTOR"
}
```

### Use the token

Include the access token in every request header:

```
Authorization: Bearer <your_access_token>
```

### Refresh expired token

```bash
POST /api/v1/auth/token/refresh/
{
    "refresh": "<your_refresh_token>"
}
```

Token lifetimes:
- Access token: **60 minutes**
- Refresh token: **7 days**

---

## 👥 User Roles & Permissions

| Role | Permissions |
|---|---|
| **ADMIN** | Full access to everything |
| **DOCTOR** | View patients, manage own appointments, update medical notes |
| **PATIENT** | Book appointments, view own medical history |
| **RECEPTIONIST** | View all appointments, book appointments for patients |

---

## 📖 API Documentation

With the server running, visit:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/api/docs/` | Swagger UI — interactive, test endpoints in browser |
| `http://127.0.0.1:8000/api/redoc/` | ReDoc — clean readable documentation |
| `http://127.0.0.1:8000/api/schema/` | Raw OpenAPI JSON schema |

In Swagger UI, click **Authorize** at the top right and paste your access token to authenticate all requests directly in the browser.

---

## 👨‍💻 Built With

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [django-redis](https://github.com/jazzband/django-redis)