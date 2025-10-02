# ✈️ Airports Service API

A web service for managing airports and booking flight tickets.  
Built with **Django 5.2.5**, **Django REST Framework**, **JWT authentication**, and auto-generated API documentation via **drf-spectacular**.  

---

## 🚀 Features
- User registration & authentication (custom User model).
- Authorization with **JWT tokens**.
- Flight and booking management.
- Request throttling (**rate limits**).
- Auto-generated API docs (Swagger / ReDoc).
- **Dockerized setup** for easy deployment.

---

## 🛠️ Tech Stack
- **Python 3.12+**
- **Django 5.2.5**
- **Django REST Framework**
- **drf-spectacular** (Swagger / ReDoc)
- **PostgreSQL**
- **Docker + docker-compose**
- **JWT (djangorestframework-simplejwt)**
- **django-debug-toolbar** (for development)

---

## 📦 Installation & Run


## ⚙️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/mileantkostya2002/drf_project
cd spy-cats-service

# You can use the fixture to see the data
python manage.py loaddata spy_cat_fixtures.json

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate     # for Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (for Django admin)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

---
## Create a .env file

- DJANGO_SECRET_KEY=your_secret_key_here
- POSTGRES_DB=airports_db
- POSTGRES_USER=airports_user
- POSTGRES_PASSWORD=airports_password
- POSTGRES_HOST=db
- POSTGRES_PORT=5432


## Run with Docker
- docker-compose up --build

## This will start:

* Django app (API)

* PostgreSQL database

## 🔑 Authentication

This project uses **JWT (JSON Web Tokens)** for authentication.
Obtain tokens via:

```
POST /api/user/token/
```

Refresh tokens via:

```
POST /api/user/token/refresh/
```

Use the token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

---

## 📖 API Documentation

Once the server is running, explore the interactive docs:

* Swagger UI: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
* ReDoc: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

```

---
## 🐾 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it as you like.
