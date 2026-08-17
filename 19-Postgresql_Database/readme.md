# NourishPak Database Documentation

## 📌 Database Purpose

The **NourishPak** database is designed to support a child nutrition and health-risk monitoring system, likely used across districts in Pakistan. It enables health workers (registered as system users) to record and track children's growth and health data, and stores machine-learning-generated **malnutrition/health risk predictions** for each child based on their recorded metrics.

The system is built around four core concerns:
1. **Geographic organization** of health data by district/province (`districts`)
2. **User authentication and role management** (`users`)
3. **Health worker profiles**, linked to a user account and assigned district (`health_worker`)
4. **Child health records** and the **ML-based risk predictions** generated from them (`children`, `prediction`)

This structure allows public health authorities to identify at-risk children early, track them by district and assigned health worker, and generate data-driven interventions.

---

## 🗂️ Tables Overview

| Table | Description |
|---|---|
| `districts` | Master list of districts/provinces used to geographically tag health workers and children |
| `users` | System accounts (login credentials & roles) used to authenticate into the platform |
| `health_worker` | Health worker profile linked to a `users` account and assigned to a `district` |
| `children` | Child records with growth metrics (age, weight, height, gender), linked to a district and the health worker who registered them |
| `prediction` | ML model output (risk score/category) generated for a specific child record |

---

## 🧱 Table Structures & Important Columns

### 1. `districts`
| Column | Type | Notes |
|---|---|---|
| **d_id** | integer | 🔑 Primary Key |
| d_name | varchar(255) | District name |
| province | varchar(255) | Province the district belongs to |
| create_at | timestamptz | Record creation timestamp |

### 2. `users`
| Column | Type | Notes |
|---|---|---|
| **u_id** | integer | 🔑 Primary Key |
| u_name | varchar(255) | Full name of the user |
| email | varchar | Login email (unique identifier for auth) |
| password | text | Hashed password |
| u_role | varchar(255) | Role, e.g. `admin`, `health_worker` |
| created_at | timestamptz | Record creation timestamp |
| updated_at | timestamptz | Record last-updated timestamp |

### 3. `health_worker`
| Column | Type | Notes |
|---|---|---|
| **h_id** | integer | 🔑 Primary Key |
| user_id | bigint | 🔗 Foreign Key → `users.u_id` |
| district_id | bigint | 🔗 Foreign Key → `districts.d_id` |
| phone | varchar(20) | Contact number |
| desgination | varchar(255) | Job title / designation |
| created_at | timestamptz | Record creation timestamp |
| updated_at | timestamptz | Record last-updated timestamp |

### 4. `children`
| Column | Type | Notes |
|---|---|---|
| **c_id** | integer | 🔑 Primary Key |
| c_name | varchar(255) | Child's name |
| age_months | integer | Age of the child in months |
| gender | varchar(255) | Gender of the child |
| weight_kg | integer | Recorded weight |
| height_cm | integer | Recorded height |
| district_id | bigint | 🔗 Foreign Key → `districts.d_id` |
| health_worker_id | bigint | 🔗 Foreign Key → `health_worker.h_id` |
| created_at | timestamptz | Record creation timestamp |
| updated_at | timestamptz | Record last-updated timestamp |

### 5. `prediction`
| Column | Type | Notes |
|---|---|---|
| **p_id** | integer | 🔑 Primary Key |
| child_id | bigint | 🔗 Foreign Key → `children.c_id` |
| risk_score | integer | Numeric ML risk score |
| risk_category | varchar(255) | e.g. `Low`, `Moderate`, `High` |
| confidence | varchar | Model confidence level |
| reasons | varchar(255) | Explanation/factors behind the prediction |
| model_name | varchar(255) | Name/version of the ML model used |
| created_at | timestamptz | Record creation timestamp |

---

## 🔑 Primary Keys

| Table | Primary Key |
|---|---|
| districts | `d_id` |
| users | `u_id` |
| health_worker | `h_id` |
| children | `c_id` |
| prediction | `p_id` |

## 🔗 Foreign Keys

| Table | Column | References |
|---|---|---|
| health_worker | `user_id` | `users(u_id)` |
| health_worker | `district_id` | `districts(d_id)` |
| children | `district_id` | `districts(d_id)` |
| children | `health_worker_id` | `health_worker(h_id)` |
| prediction | `child_id` | `children(c_id)` |

---

## 🔄 Table Relationships

- **districts → health_worker** (1 : many) — one district can have many health workers.
- **districts → children** (1 : many) — one district contains many children's records.
- **users → health_worker** (1 : many) — one user account maps to a health worker profile (typically 1:1 in practice, modeled as 1:many).
- **health_worker → children** (1 : many) — one health worker registers/manages many children.
- **children → prediction** (1 : many) — one child can have multiple risk predictions over time (e.g., re-assessments).

**Relationship chain:**
```
districts ──┬── health_worker ──┐
            │                   ├── children ── prediction
            └───────────────────┘
users ── health_worker
```

---

## 🖼️ ER Diagram

The entity-relationship diagram (`nourishpak_database_er_diagram.png`) shows five tables:

```
┌────────────┐        ┌────────────────┐        ┌──────────────┐        ┌──────────────┐
│  districts │──1:M──▶│  health_worker  │◀──M:1──│    users     │        │              │
│  d_id (PK) │        │  h_id (PK)      │        │  u_id (PK)   │        │              │
└─────┬──────┘        │  user_id (FK)   │        └──────────────┘        │              │
      │                │  district_id(FK)│                                │              │
      │1:M             └────────┬────────┘                                │              │
      │                          │1:M                                     │              │
      ▼                          ▼                                        │              │
┌────────────────────────────────────────┐                                │              │
│              children                  │                                │              │
│  c_id (PK)                              │                                │              │
│  district_id (FK) / health_worker_id(FK)│                                │              │
└──────────────────┬───────────────────────┘                              │              │
                    │ 1:M                                                  │              │
                    ▼                                                      │              │
            ┌───────────────┐                                              │              │
            │  prediction   │                                              │              │
            │  p_id (PK)    │                                              │              │
            │  child_id(FK) │                                              │              │
            └───────────────┘
```

---

## 🧪 Sample Queries

**Get all children in a specific district:**
```sql
SELECT c_id, c_name, age_months, gender, weight_kg, height_cm
FROM children
WHERE district_id = 3;
```

**Get all health workers and their contact info:**
```sql
SELECT h_id, phone, desgination
FROM health_worker
WHERE district_id = 5;
```

**Get all high-risk predictions:**
```sql
SELECT p_id, child_id, risk_score, risk_category
FROM prediction
WHERE risk_category = 'High'
ORDER BY risk_score DESC;
```

**Count children registered per district:**
```sql
SELECT d.d_name, COUNT(c.c_id) AS total_children
FROM districts d
LEFT JOIN children c ON d.d_id = c.district_id
GROUP BY d.d_name;
```

---

## 🔗 JOIN Queries

**Children with their district and assigned health worker:**
```sql
SELECT 
    c.c_id, c.c_name, c.age_months,
    d.d_name AS district,
    u.u_name AS health_worker_name,
    hw.phone AS health_worker_phone
FROM children c
JOIN districts d ON c.district_id = d.d_id
JOIN health_worker hw ON c.health_worker_id = hw.h_id
JOIN users u ON hw.user_id = u.u_id;
```

**Full prediction report — child + risk + who registered them:**
```sql
SELECT 
    ch.c_name,
    ch.age_months,
    ch.gender,
    p.risk_score,
    p.risk_category,
    p.confidence,
    p.model_name,
    d.d_name AS district,
    u.u_name AS registered_by
FROM prediction p
JOIN children ch ON p.child_id = ch.c_id
JOIN districts d ON ch.district_id = d.d_id
JOIN health_worker hw ON ch.health_worker_id = hw.h_id
JOIN users u ON hw.user_id = u.u_id
ORDER BY p.created_at DESC;
```

**All health workers with their user login and district:**
```sql
SELECT 
    u.u_name, u.email, u.u_role,
    hw.phone, hw.desgination,
    d.d_name AS district, d.province
FROM health_worker hw
JOIN users u ON hw.user_id = u.u_id
JOIN districts d ON hw.district_id = d.d_id;
```

**Average risk score by district:**
```sql
SELECT 
    d.d_name,
    ROUND(AVG(p.risk_score), 2) AS avg_risk_score,
    COUNT(p.p_id) AS total_predictions
FROM prediction p
JOIN children c ON p.child_id = c.c_id
JOIN districts d ON c.district_id = d.d_id
GROUP BY d.d_name
ORDER BY avg_risk_score DESC;
```

---

## ⚙️ Connecting to FastAPI Backend

This PostgreSQL database is designed to be consumed by a **FastAPI** backend using an ORM (typically **SQLAlchemy** or **SQLModel**) with **Pydantic** schemas for request/response validation. Recommended integration approach:

### 1. Connection setup
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://<user>:<password>@<host>:<port>/nourishpak"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. ORM Models mirror the ER diagram
Each table (`districts`, `users`, `health_worker`, `children`, `prediction`) becomes a SQLAlchemy model, with `relationship()` fields mapping the foreign keys shown in the diagram (e.g., `children.health_worker_id → health_worker.h_id`).

### 3. Pydantic schemas
Separate `Create`, `Update`, and `Response` schemas per table are used for FastAPI request/response validation — e.g. `ChildCreate`, `ChildResponse`, `PredictionResponse`.

### 4. API layer structure
```
app/
├── models/          # SQLAlchemy models (districts, users, health_worker, children, prediction)
├── schemas/         # Pydantic request/response schemas
├── routers/         # FastAPI route handlers (e.g. /children, /predictions, /health-workers)
├── crud/            # DB query/CRUD logic
├── database.py      # Engine & session setup
└── main.py          # FastAPI app entrypoint
```

### 5. Typical endpoint flow
- `POST /children` → health worker registers a new child → row inserted into `children`
- `POST /predictions` → ML model runs on a child's data → result inserted into `prediction`, linked via `child_id`
- `GET /districts/{id}/children` → JOIN query returning all children in a district
- `GET /children/{id}/predictions` → JOIN query returning prediction history for a child

### 6. Authentication
The `users` table (with `email`, `password`, `u_role`) backs a JWT-based authentication flow in FastAPI (e.g. via `fastapi-users` or a custom `OAuth2PasswordBearer` implementation), where `u_role` determines access control (e.g. `admin` vs `health_worker` permissions).

This design keeps the database schema and FastAPI application layer in sync — every foreign key relationship shown in the ER diagram becomes a corresponding SQLAlchemy `relationship()` and a nested field in the API's JSON responses.