# 💰 Finance Backend System (FastAPI + PostgreSQL)

A backend system for managing financial records with **role-based access control**, **JWT authentication (HttpOnly cookies)**, and **dashboard analytics**.

---

## 🚀 Features

### 🔐 Authentication & Security

* JWT-based authentication (Access + Refresh tokens)
* Tokens stored in **HttpOnly cookies** (prevents XSS attacks)
* Refresh token rotation with database tracking (JTI-based)
* Secure password hashing using bcrypt

### 👥 Role-Based Access Control (RBAC)

* **Admin** → Full access (users + records)
* **Analyst** → View records + dashboard insights
* **Viewer** → Read-only access

### 💰 Financial Records Management

* Create, update, delete financial records
* Fields:

  * Amount
  * Type (Income / Expense)
  * Category
  * Date
  * Notes
* Filtering support:

  * By date
  * By category
  * By type

### 📊 Dashboard Analytics

* Total income
* Total expenses
* Net balance
* Category-wise aggregation
* Recent activity
* Trend-based summaries

### 🧱 Backend Architecture

* Clean separation:

  * **Router** → HTTP layer
  * **Service** → Business logic
  * **DAO** → Database access
  * **Models** → ORM layer
* Async-first design using FastAPI + SQLAlchemy

### ⚙️ Database & Migrations

* PostgreSQL database
* SQLAlchemy ORM (async)
* Alembic for schema migrations

---

## 🧠 Design Highlights

* **HttpOnly cookies over localStorage**
  → prevents token theft via XSS

* **Refresh token stored in DB**
  → allows revocation and session control

* **SQL-based aggregation**
  → efficient dashboard queries (no Python loops)

* **Async architecture**
  → scalable and non-blocking

* **Extensible rate limiting (Redis-ready)**
  → rate limiting logic implemented but not enforced in routers yet

---

## ⚠️ Rate Limiting Note

Redis-based rate limiting is implemented in the codebase but **not currently applied to API routes**.

This was intentionally kept optional to:

* Keep the core system simple
* Allow easy integration in future by adding decorators/middleware

---

## 📁 Project Structure

```bash
app/
 ├── auth/              # Authentication module
 ├── users/             # User management
 ├── records/           # Financial records
 ├── dashboard/         # Analytics APIs
 ├── categories/        
 ├── repositories/
 ├── models/            # SQLAlchemy models
 ├── core/              # Config, security, cookies
 ├── db/                # Database session
 ├── main.py            # Entry point

alembic/                # DB migrations
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd finance_backend
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv env
env\Scripts\activate   # Windows
# OR
source env/bin/activate  # Linux/Mac
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/finance_db
SECRET_KEY=your_secret_key

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

COOKIE_SECURE=False
COOKIE_SAMESITE=lax

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 5️⃣ Run database migrations

```bash
alembic upgrade head
```

---

### 6️⃣ Start the server

```bash
uvicorn app.main:app --reload
```

---

### 🌐 Access API

```bash
http://localhost:8000
```

---

## 🔐 Authentication Flow

1. User registers/logs in
2. Server sets:

   * `access_token` (short-lived)
   * `refresh_token` (long-lived)
3. Cookies are:

   * HttpOnly
   * Secure (in production)
4. Access token used for requests
5. Refresh endpoint rotates tokens

---

## 📡 API Endpoints

### Auth

```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/user/me
```

### Records

```
POST   /api/v1/records
GET    /api/v1/records
PATCH    /api/v1/records/{id}
DELETE /api/v1/records/{id}
```

### Dashboard

```
GET /api/v1/dashboard/summary
GET /api/v1/dashboard/trends
GET /api/v1/dashboard/categories
GET /api/v1/dashboard/recent

```

---

## 🧪 Validation & Error Handling

* Strong password validation (length, uppercase, lowercase, digits, special chars)
* Proper HTTP status codes
* Clear error messages
* Protection against invalid operations

---

## ⚠️ Assumptions

* Single-tenant system
* Categories are pre-defined or managed separately
* No frontend required (API-focused assignment)

---

## 🔮 Future Improvements

* Enable Redis rate limiting on all endpoints
* Add pagination + search
* Add unit & integration tests
* Introduce caching for dashboard APIs
* Add CI/CD pipeline
* Dockerize for deployment

---

## 🧠 Summary

This project demonstrates:

* Backend system design
* Clean architecture principles
* Secure authentication handling
* Efficient data modeling and querying
* Real-world API design practices

---

## 👨‍💻 Author

Shiva Sundar R
