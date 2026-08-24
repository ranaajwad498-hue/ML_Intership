# Authentication System — JWT with FastAPI & PostgreSQL

A REST API authentication system built with **FastAPI**, **PostgreSQL**, and **JWT (JSON Web Tokens)**, supporting role-based access control for `admin` and `health_worker` user roles.

---

## Table of Contents

- [What is JWT?](#what-is-jwt)
- [Authentication vs Authorization](#authentication-vs-authorization)
- [Password Hashing](#password-hashing)
- [Login Process](#login-process)
- [JWT Token Generation](#jwt-token-generation)
- [Token Expiry](#token-expiry)
- [Protected Routes](#protected-routes)
- [Admin Permissions](#admin-permissions)
- [Health Worker Permissions](#health-worker-permissions)
- [401 vs 403](#401-vs-403)
- [Sample Login Request & Response](#sample-login-request--response)
- [Complete Authentication Flow](#complete-authentication-flow)

---

## What is JWT?

**JWT (JSON Web Token)** is a compact, self-contained way to securely transmit information between two parties as a JSON object. It's commonly used to represent a user's identity and permissions after they log in.

A JWT has three parts, separated by dots (`.`):

```
header.payload.signature
```

| Part | Purpose |
|------|---------|
| **Header** | Specifies the token type (`JWT`) and signing algorithm (e.g. `HS256`) |
| **Payload** | Contains claims — data about the user (e.g. `sub`, `exp`, `role`) |
| **Signature** | Verifies the token wasn't tampered with, using a secret key |

Because the signature is created with a server-side secret key, the server can trust the contents of the token **without needing to check the database on every request** — it just verifies the signature and reads the payload.

> ⚠️ JWT payloads are **base64-encoded, not encrypted**. Never put sensitive data (passwords, secrets) inside a JWT payload — anyone can decode it and read it, they just can't *forge* a valid one without the secret key.

---

## Authentication vs Authorization

These two terms are often confused but mean very different things:

| | Authentication | Authorization |
|---|---|---|
| **Question it answers** | "Who are you?" | "What are you allowed to do?" |
| **When it happens** | At login | On every request to a protected resource |
| **In this system** | Verifying email/password match during `/login` | Checking `u_role` (e.g. `admin` vs `health_worker`) before allowing an action |
| **Failure response** | `401 Unauthorized` | `403 Forbidden` |

**In short:** authentication confirms your identity. Authorization decides what your identity is *permitted* to do.

---

## Password Hashing

Passwords are **never stored in plain text**. Instead, they're run through a one-way hashing algorithm (this project uses **bcrypt** via `pwdlib`) before being saved to the database.

```python
def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)
```

**Why hashing matters:**
- Hashing is **one-directional** — you can't reverse a hash back into the original password.
- Bcrypt automatically applies a random **salt** to each password, so two users with the same password get completely different hashes.
- Even if the database is leaked, attackers can't directly read user passwords.
- On login, the plaintext password the user submits is hashed-compared against the stored hash — the original password is never stored or compared directly.

---

## Login Process

1. User submits `email`/`username` and `password` to `POST /login`.
2. The server looks up the user record by email/username in PostgreSQL.
3. The submitted password is verified against the stored hash using `verify_password()`.
4. If verification **fails** → `401 Unauthorized` is returned, no token is issued.
5. If verification **succeeds** → a JWT access token is generated and returned to the client.

---

## JWT Token Generation

After successful authentication, the server creates a signed JWT containing claims that identify the user:

```python
access_token = AuthService.create_access_token(data={"sub": str(user.u_id)})
```

A typical payload includes:

```json
{
  "sub": "42",
  "exp": 1729612345
}
```

| Claim | Meaning |
|-------|---------|
| `sub` | "Subject" — identifies the user (commonly the user ID) |
| `exp` | Expiry timestamp (Unix time) — after this, the token is rejected |
| `iat` *(optional)* | "Issued at" — when the token was created |
| `role` *(optional)* | User's role, if embedded directly in the token for quick access checks |

The token is signed using a secret key and algorithm (e.g. `HS256`), so any tampering with the payload invalidates the signature and the token is rejected on verification.

---

## Token Expiry

JWTs are issued with a limited lifespan via the `exp` claim. This limits the damage if a token is ever leaked or stolen.

- Short-lived tokens (e.g. 15–60 minutes) are generally used for access tokens.
- Once expired, the token is rejected with `401 Unauthorized`, even if the signature is valid — the user must log in again (or use a refresh token, if implemented) to get a new one.
- The server checks expiry automatically during decoding — an expired token raises `ExpiredSignatureError`.

```python
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except jwt.ExpiredSignatureError:
    # token is expired — reject with 401
    ...
```

---

## Protected Routes

Protected routes require a valid JWT to be accessed. The client must send the token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

In FastAPI, this is enforced via a dependency:

```python
@app.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
```

`get_current_user`:
1. Extracts the token from the request header (via `oauth2_scheme`).
2. Decodes and verifies the JWT signature and expiry.
3. Looks up the user in the database using the ID from the token payload.
4. Returns the user object, or raises `401`/`404` if invalid.

Any route depending on `get_current_user` is automatically protected — unauthenticated requests never reach the route's logic.

---

## Admin Permissions

Users with `u_role = "admin"` typically have elevated access, such as:

- Viewing, creating, updating, or deleting **any** user account
- Managing roles/permissions for other users
- Accessing system-wide data, audit logs, or reports
- Overriding restrictions that apply to regular users

Example role-check dependency:

```python
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.u_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

---

## Health Worker Permissions

Users with `u_role = "health_worker"` typically have access scoped to their operational duties, such as:

- Viewing and updating patient/case records assigned to them
- Submitting reports or entries relevant to their role
- Read-only access to certain shared resources
- **No** access to admin-level actions (user management, system settings)

Example role-check dependency:

```python
def require_health_worker(current_user: User = Depends(get_current_user)):
    if current_user.u_role != "health_worker":
        raise HTTPException(status_code=403, detail="Health worker access required")
    return current_user
```

> Adjust the exact permission boundaries above to match your application's actual business logic — these are illustrative defaults.

---

## 401 vs 403

These two status codes are frequently mixed up:

| Code | Meaning | When it's returned |
|------|---------|---------------------|
| **401 Unauthorized** | "I don't know who you are" | Missing token, invalid token, expired token, wrong login credentials |
| **403 Forbidden** | "I know who you are, but you can't do this" | Valid, authenticated user tries to access a resource their role doesn't permit |

**Rule of thumb:**
- No valid identity at all → `401`
- Valid identity, but insufficient permissions → `403`

---

## Sample Login Request & Response

**Request:**

```http
POST /login
Content-Type: application/json

{
  "email": "worker@example.com",
  "password": "SecurePass123!"
}
```

**Success Response — `200 OK`:**

```json
{
  "message": "Login Successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsImV4cCI6MTcyOTYxMjM0NX0.abc123signature",
  "token_type": "bearer",
  "u_role": "health_worker"
}
```

**Failure Response — `401 Unauthorized`:**

```json
{
  "detail": "Invalid email or password"
}
```

**Using the token on a protected route:**

```http
GET /me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsImV4cCI6MTcyOTYxMjM0NX0.abc123signature
```

---

## Complete Authentication Flow

```
┌──────────┐                         ┌──────────┐                       ┌─────────────┐
│  Client  │                         │  FastAPI │                       │  PostgreSQL │
└────┬─────┘                         └────┬─────┘                       └──────┬──────┘
     │                                    │                                    │
     │  1. POST /signup (email, pwd)      │                                    │
     ├───────────────────────────────────>│                                    │
     │                                    │  2. hash_password(pwd)             │
     │                                    │  3. INSERT user (hashed pwd)       │
     │                                    ├───────────────────────────────────>│
     │                                    │<───────────────────────────────────┤
     │  4. 201 Created (user info)        │                                    │
     │<───────────────────────────────────┤                                    │
     │                                    │                                    │
     │  5. POST /login (email, pwd)       │                                    │
     ├───────────────────────────────────>│                                    │
     │                                    │  6. SELECT user by email           │
     │                                    ├───────────────────────────────────>│
     │                                    │<───────────────────────────────────┤
     │                                    │  7. verify_password(pwd, hash)     │
     │                                    │  8. create_access_token({sub, exp})│
     │  9. 200 OK (JWT access_token)      │                                    │
     │<───────────────────────────────────┤                                    │
     │                                    │                                    │
     │  10. GET /me                       │                                    │
     │     Authorization: Bearer <token>  │                                    │
     ├───────────────────────────────────>│                                    │
     │                                    │  11. decode & verify JWT           │
     │                                    │  12. SELECT user by id from token  │
     │                                    ├───────────────────────────────────>│
     │                                    │<───────────────────────────────────┤
     │  13. 200 OK (user data)            │                                    │
     │<───────────────────────────────────┤                                    │
     │                                    │                                    │
     │  14. GET /admin-only-route         │                                    │
     ├───────────────────────────────────>│                                    │
     │                                    │  15. valid token, but role check   │
     │                                    │      fails (u_role != "admin")     │
     │  16. 403 Forbidden                 │                                    │
     │<───────────────────────────────────┤                                    │
```

**Step-by-step summary:**

1. User registers via `/signup` — password is hashed before storage, never stored in plain text.
2. User logs in via `/login` with email + password.
3. Server verifies the password against the stored hash.
4. On success, server issues a signed JWT containing the user's ID (`sub`) and expiry (`exp`).
5. Client stores the token (e.g. in memory, secure storage) and sends it as `Authorization: Bearer <token>` on subsequent requests.
6. For protected routes, the server decodes and verifies the token's signature and expiry.
7. If valid, the server fetches the corresponding user from the database and attaches it to the request.
8. If the route also requires a specific role (e.g. `admin`), the server checks `u_role` and returns `403` if it doesn't match — even though the token itself was valid.
9. If the token is missing, invalid, or expired at any point, the server returns `401 Unauthorized`.

---

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **pwdlib (bcrypt)** — password hashing
- **PyJWT** — JWT encoding/decoding