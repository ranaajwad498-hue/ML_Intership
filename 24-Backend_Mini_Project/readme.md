# Child Health Prediction API

A FastAPI backend for managing child health records and predicting malnutrition/growth risk using a machine learning model, backed by PostgreSQL.

> This README is a template. Sections marked `TODO` or using placeholder values should be updated to match your actual implementation.

---

## 1. Backend Architecture

```
Client (Web / Mobile / Swagger UI)
        │
        ▼
   FastAPI App
        │
   ┌────┴─────────────────────┐
   │                          │
Routers (API Layer)     Middleware (JWT Auth, CORS)
   │
   ▼
Services (Business Logic)
   │  - ChildService
   │  - PredictionService
   │  - AuthService
   ▼
Models (SQLAlchemy ORM)
   │
   ▼
PostgreSQL Database
```

- **FastAPI** handles routing, request validation (via Pydantic schemas), and response serialization.
- **Service layer** (`PredictionService`, `ChildService`, etc.) contains business logic, keeping route handlers thin.
- **SQLAlchemy ORM** models map Python classes to PostgreSQL tables.
- **ML model** (Random Forest, loaded via `joblib`/`pickle`) is loaded once at startup and reused across requests.
- **JWT middleware/dependencies** protect routes and enforce role-based access.

---

## 2. PostgreSQL Integration

- **ORM:** SQLAlchemy
- **Driver:** `psycopg2` (or `asyncpg` if using async engine)
- **Connection:** configured via environment variable

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db_name>
```

`app/database.py` (TODO: confirm filename) sets up the engine and session:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Migrations:** TODO — specify if using Alembic (`alembic upgrade head`) or `Base.metadata.create_all(bind=engine)`.

---

## 3. JWT Authentication

Authentication uses **JSON Web Tokens (JWT)**.

- **Login endpoint** issues an access token (and optionally a refresh token) on valid credentials.
- **Protected routes** require a `Bearer` token in the `Authorization` header.
- Tokens are decoded via a dependency (e.g. `get_current_user`) that FastAPI injects into any route needing authentication.

```
Authorization: Bearer <access_token>
```

**Token payload example:**
```json
{
  "sub": "user_id",
  "role": "clinician",
  "exp": 1730000000
}
```

**Environment variables:**
```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 4. Roles and Permissions

TODO: confirm your actual roles. Example structure:

| Role        | Description                          | Permissions                                              |
|-------------|---------------------------------------|-----------------------------------------------------------|
| `admin`     | Full system access                    | Manage users, all CRUD, all predictions                   |
| `clinician` | Healthcare worker / doctor            | Create/view/update children, run predictions, view history|
| `viewer`    | Read-only access                      | View children and predictions only                        |

Role is embedded in the JWT and checked via a dependency, e.g.:

```python
def require_role(*allowed_roles):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return checker
```

---

## 5. Child CRUD APIs

Standard Create / Read / Update / Delete endpoints for child records (see full endpoint table in Section 7).

- Create a child profile
- List all children (optionally paginated/filtered)
- Get a single child by ID
- Update a child's details
- Delete a child record

---

## 6. ML Prediction API

- **Model:** Random Forest Classifier (loaded from `app/ml_models/Random Forest Model.pkl`)
- **Input features:** `Age (months)`, `Gender`, `Household_Wealth_Index`, `Height_cm`, `Mother_Education`, `Weight_kg`
- **Output:** `risk_score` (0–100), `risk_category` (`Low Risk` / `Medium Risk` / `High Risk`), `confidence`, and generated `advice`

**Flow:**
1. Client calls `POST /children/{child_id}/predict`.
2. Backend fetches the child's stored data from PostgreSQL.
3. `PredictionService.prepare_input()` builds the feature DataFrame.
4. `PredictionService.calculate_risk_score()` runs the model.
5. Risk category and advice are derived.
6. Result is saved to the `prediction` table and returned to the client.

---

## 7. Prediction History

Every prediction run is stored (not overwritten), so a child can have multiple prediction records over time.

- `GET /children/{child_id}/predictions` — full history for one child
- `GET /children/{child_id}/predict/latest` — most recent prediction for one child
- `GET /predict/latest` — most recent prediction across the entire system

---

## 8. All API Endpoints

TODO: replace with your actual 12 endpoints. Template based on what's been discussed:

| # | Method | Endpoint                                | Auth Required | Description                              |
|---|--------|------------------------------------------|----------------|-------------------------------------------|
| 1 | POST   | `/auth/register`                         | No             | Register a new user                        |
| 2 | POST   | `/auth/login`                            | No             | Login, returns JWT access token            |
| 3 | POST   | `/auth/refresh`                          | Yes            | Refresh access token                       |
| 4 | GET    | `/auth/me`                               | Yes            | Get current logged-in user info            |
| 5 | POST   | `/children`                              | Yes            | Create a new child record                  |
| 6 | GET    | `/children`                              | Yes            | List all children                          |
| 7 | GET    | `/children/{child_id}`                   | Yes            | Get a single child by ID                   |
| 8 | PUT    | `/children/{child_id}`                   | Yes            | Update a child's record                    |
| 9 | DELETE | `/children/{child_id}`                   | Yes            | Delete a child's record                    |
| 10| POST   | `/children/{child_id}/predict`           | Yes            | Run a new ML prediction for a child        |
| 11| GET    | `/children/{child_id}/predict/latest`    | Yes            | Get latest prediction for a specific child |
| 12| GET    | `/predict/latest`                        | Yes            | Get latest prediction across all children  |

---

## 9. Request & Response Examples

### Login
**Request:** `POST /auth/login`
```json
{
  "username": "clinician1",
  "password": "securepassword"
}
```
**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Child
**Request:** `POST /children`
```json
{
  "name": "Ayesha",
  "age_months": 24,
  "gender": "female",
  "household_wealth_index": 3,
  "height_cm": 82.5,
  "mother_education": "secondary",
  "weight_kg": 10.2
}
```
**Response:** `201 Created`
```json
{
  "c_id": 5,
  "name": "Ayesha",
  "age_months": 24,
  "gender": "female",
  "household_wealth_index": 3,
  "height_cm": 82.5,
  "mother_education": "secondary",
  "weight_kg": 10.2
}
```

### Run Prediction
**Request:** `POST /children/5/predict`
(no body needed — pulls stored child data)

**Response:** `200 OK`
```json
{
  "p_id": 12,
  "child_id": 5,
  "risk_score": 78,
  "risk_category": "High Risk",
  "confidence": 78.42,
  "advice": "Refer child for nutrition support and further clinical assessment.",
  "created_at": "2026-09-12T10:15:00+05:00"
}
```

### Get Latest Prediction (system-wide)
**Request:** `GET /predict/latest`

**Response:** `200 OK`
```json
{
  "p_id": 12,
  "child_id": 5,
  "risk_score": 78,
  "risk_category": "High Risk",
  "confidence": 78.42,
  "advice": "Refer child for nutrition support and further clinical assessment.",
  "created_at": "2026-09-12T10:15:00+05:00"
}
```

---

## 10. Error Handling

Standard error responses use FastAPI's `HTTPException` and follow this shape:

```json
{
  "detail": "Child not found in the database"
}
```

| Status Code | Meaning                          | Example Scenario                          |
|-------------|-----------------------------------|---------------------------------------------|
| 400         | Bad Request                       | Invalid or malformed input data              |
| 401         | Unauthorized                      | Missing or invalid JWT token                 |
| 403         | Forbidden                         | Valid token, but role lacks permission       |
| 404         | Not Found                         | Child ID or prediction record doesn't exist  |
| 422         | Unprocessable Entity              | Request body fails Pydantic validation       |
| 500         | Internal Server Error             | Unhandled exception / model failure          |

Validation errors (422) return FastAPI's default structure:
```json
{
  "detail": [
    {
      "loc": ["body", "age_months"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 11. Project Folder Structure

TODO: adjust to match your actual layout.

```
project-root/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth/
│   │   ├── jwt_handler.py
│   │   └── dependencies.py
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── child_router.py
│   │   └── prediction_router.py
│   ├── services/
│   │   ├── prediction_service.py
│   │   └── child_service.py
│   └── ml_models/
│       └── Random Forest Model.pkl
├── requirements.txt
├── .env
└── README.md
```

---

## 12. How to Run the Backend

```bash
git clone <your-repo-url>
cd project-root

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/child_health_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run database migrations (if using Alembic):
```bash
alembic upgrade head
```

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```

---

## 13. Swagger / API Docs

FastAPI auto-generates interactive documentation:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **OpenAPI schema:** `http://127.0.0.1:8000/openapi.json`

---

## 14. Complete Testing Flow

1. **Register a user** — `POST /auth/register`
2. **Login** — `POST /auth/login` → copy the `access_token`
3. **Authorize in Swagger** — click "Authorize" in `/docs`, paste `Bearer <token>`
4. **Create a child** — `POST /children`
5. **Verify child exists** — `GET /children/{child_id}`
6. **Run a prediction** — `POST /children/{child_id}/predict`
7. **Check latest prediction for that child** — `GET /children/{child_id}/predict/latest`
8. **Check system-wide latest prediction** — `GET /predict/latest`
9. **Update the child's data** — `PUT /children/{child_id}`
10. **Re-run prediction** and confirm a new history record was created (not overwritten)
11. **Delete the child** — `DELETE /children/{child_id}`
12. **Confirm cascading behavior** — check whether related predictions are deleted or retained (TODO: define your intended behavior)

---

## License

TODO: add license.
