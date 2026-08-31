# FastAPI File Upload Service

A secure file upload system built with **FastAPI**, **PostgreSQL**, and **JWT authentication**, supporting profile photo uploads and general document management (upload, list, delete).

---

## Table of Contents

1. [How FastAPI File Upload Works](#how-fastapi-file-upload-works)
2. [Allowed File Types](#allowed-file-types)
3. [Maximum File Sizes](#maximum-file-sizes)
4. [File Validation](#file-validation)
5. [File Naming Strategy](#file-naming-strategy)
6. [Upload Folder Structure](#upload-folder-structure)
7. [PostgreSQL Fields/Tables Used](#postgresql-fieldstables-used)
8. [Profile Photo Upload API](#profile-photo-upload-api)
9. [Document Upload API](#document-upload-api)
10. [Document Listing API](#document-listing-api)
11. [Document Deletion API](#document-deletion-api)
12. [JWT Protection](#jwt-protection)
13. [Sample Requests and Responses](#sample-requests-and-responses)
14. [Security Considerations](#security-considerations)

---

## How FastAPI File Upload Works

FastAPI handles file uploads using the `UploadFile` class from `fastapi`, combined with `File(...)` as a dependency marker. Under the hood, `UploadFile` wraps Python's `SpooledTemporaryFile`, which means:

- Files are streamed to a **temporary spooled buffer** (memory up to a threshold, then disk) rather than being loaded entirely into RAM at once.
- FastAPI exposes async methods (`await file.read()`, `await file.write()`, `await file.seek()`) so I/O doesn't block the event loop.
- The endpoint receives `multipart/form-data` requests — this is required because JSON cannot carry binary payloads.

Basic pattern used throughout this project:

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # validate, then save to disk
    with open(destination_path, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "content_type": file.content_type}
```

For large files, we avoid loading everything into memory with `.read()` and instead stream in chunks:

```python
import shutil

async def save_upload(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
```

---

## Allowed File Types

File type validation happens on both **extension** and **MIME type** (content-type) to reduce spoofing risk.

### Profile Photos

| Extension | MIME Type |
|-----------|-----------|
| `.jpg` / `.jpeg` | `image/jpeg` |
| `.png` | `image/png` |
| `.webp` | `image/webp` |

### Documents

| Extension | MIME Type |
|-----------|-----------|
| `.pdf` | `application/pdf` |
| `.doc` | `application/msword` |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| `.xls` | `application/vnd.ms-excel` |
| `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| `.png` / `.jpg` / `.jpeg` | image scans |

```python
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_DOCUMENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "image/jpeg",
    "image/png",
}
```

---

## Maximum File Sizes

| Upload Type | Max Size |
|-------------|----------|
| Profile Photo | 5 MB |
| Document | 20 MB |

Size limits are enforced **after reading the stream**, comparing byte length against a constant, since `UploadFile` does not expose size directly without reading:

```python
MAX_PROFILE_PHOTO_SIZE = 5 * 1024 * 1024   # 5 MB
MAX_DOCUMENT_SIZE = 20 * 1024 * 1024       # 20 MB

async def validate_size(file: UploadFile, max_size: int):
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    await file.seek(0)  # reset pointer for later reads
    return contents
```

We also configure a reverse-proxy-level limit (e.g., `client_max_body_size` in Nginx) as a first line of defense, so oversized uploads are rejected before reaching the app.

---

## File Validation

Validation is layered — each layer catches what the previous one might miss:

1. **Extension check** — reject disallowed extensions outright.
2. **MIME type check** — cross-check `file.content_type` against the allow-list.
3. **Magic-byte / signature check** — use `python-magic` to inspect actual file bytes, since `content_type` can be spoofed by the client.
4. **Size check** — reject files over the limit.
5. **Filename sanitization** — strip path components and dangerous characters.

```python
import magic
from pathlib import Path

def validate_file(file: UploadFile, contents: bytes, allowed_mimes: set, allowed_exts: set):
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_exts:
        raise HTTPException(400, f"Extension {ext} not allowed")

    detected_mime = magic.from_buffer(contents, mime=True)
    if detected_mime not in allowed_mimes:
        raise HTTPException(400, f"File type {detected_mime} not allowed")

    if file.content_type not in allowed_mimes:
        raise HTTPException(400, "Declared content-type mismatch")
```

---

## File Naming Strategy

Original filenames are **never trusted** and never used directly on disk. Instead:

- Generate a random UUID4 as the base filename.
- Preserve only the (validated) extension.
- Store the original filename separately in the database for display purposes.

```python
import uuid
from pathlib import Path

def generate_filename(original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4().hex}{ext}"
```

This prevents:
- Path traversal (`../../etc/passwd`)
- Filename collisions
- Leaking of user-supplied strings into the filesystem

---

## Upload Folder Structure

Files are organized by upload type and user ID to keep storage manageable and access-controlled:

```
/uploads
├── profile_photos/
│   └── {user_id}/
│       └── {uuid}.jpg
├── documents/
│   └── {user_id}/
│       └── {uuid}.pdf
└── tmp/
    └── {uuid}.part      # partial/in-progress uploads (cleaned periodically)
```

```python
import os

def get_upload_path(upload_type: str, user_id: int, filename: str) -> str:
    base_dir = os.path.join("uploads", upload_type, str(user_id))
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)
```

In production, `uploads/` typically maps to an object store (S3, GCS, Azure Blob) rather than local disk — the same path structure is used as the object **key** prefix.

---

## PostgreSQL Fields/Tables Used

### `users` table (relevant columns)

| Column | Type | Notes |
|--------|------|-------|
| `id` | `SERIAL PRIMARY KEY` | |
| `email` | `VARCHAR(255) UNIQUE` | |
| `profile_photo_path` | `VARCHAR(500)` | nullable, stores relative path/key |
| `created_at` | `TIMESTAMP` | |

### `documents` table

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID PRIMARY KEY` | matches stored filename |
| `user_id` | `INTEGER REFERENCES users(id)` | owner, indexed |
| `original_filename` | `VARCHAR(255)` | user-facing name |
| `stored_filename` | `VARCHAR(255)` | UUID-based name on disk |
| `file_path` | `VARCHAR(500)` | full storage path/key |
| `file_type` | `VARCHAR(100)` | MIME type |
| `file_size` | `BIGINT` | bytes |
| `uploaded_at` | `TIMESTAMP DEFAULT now()` | |
| `is_deleted` | `BOOLEAN DEFAULT false` | soft delete flag |

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT false
);

CREATE INDEX idx_documents_user_id ON documents(user_id);
```

SQLAlchemy model equivalent:

```python
from sqlalchemy import Column, String, BigInteger, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
```

---

## Profile Photo Upload API

```
POST /api/v1/users/me/profile-photo
```

- **Auth**: Required (JWT bearer token)
- **Content-Type**: `multipart/form-data`
- **Field**: `file`

```python
@router.post("/users/me/profile-photo", status_code=200)
async def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contents = await validate_size(file, MAX_PROFILE_PHOTO_SIZE)
    validate_file(file, contents, ALLOWED_IMAGE_TYPES, {".jpg", ".jpeg", ".png", ".webp"})

    filename = generate_filename(file.filename)
    path = get_upload_path("profile_photos", current_user.id, filename)

    with open(path, "wb") as f:
        f.write(contents)

    current_user.profile_photo_path = path
    db.commit()

    return {"message": "Profile photo updated", "path": path}
```

---

## Document Upload API

```
POST /api/v1/documents
```

- **Auth**: Required
- **Content-Type**: `multipart/form-data`
- **Field**: `file`

```python
@router.post("/documents", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contents = await validate_size(file, MAX_DOCUMENT_SIZE)
    validate_file(file, contents, ALLOWED_DOCUMENT_TYPES, ALLOWED_DOC_EXTS)

    stored_filename = generate_filename(file.filename)
    path = get_upload_path("documents", current_user.id, stored_filename)

    with open(path, "wb") as f:
        f.write(contents)

    doc = Document(
        user_id=current_user.id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=path,
        file_type=file.content_type,
        file_size=len(contents),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc
```

---

## Document Listing API

```
GET /api/v1/documents
```

- **Auth**: Required
- Returns only documents owned by the authenticated user, excluding soft-deleted rows.

```python
@router.get("/documents")
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    docs = (
        db.query(Document)
        .filter(Document.user_id == current_user.id, Document.is_deleted == False)
        .order_by(Document.uploaded_at.desc())
        .all()
    )
    return docs
```

---

## Document Deletion API

```
DELETE /api/v1/documents/{document_id}
```

- **Auth**: Required
- Ownership is verified before deletion; other users' documents return `404` (not `403`, to avoid leaking existence).
- Implemented as a **soft delete**; the physical file is removed by a separate cleanup job or immediately, depending on retention policy.

```python
@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == current_user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc.is_deleted = True
    db.commit()

    # optional: remove physical file immediately
    # os.remove(doc.file_path)

    return
```

---

## JWT Protection

All upload/list/delete endpoints depend on `get_current_user`, which decodes and verifies the bearer token on every request.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = "..."   # loaded from environment, never hardcoded
ALGORITHM = "HS256"

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

Every route in this document uses `Depends(get_current_user)`, so requests without a valid, non-expired token receive `401 Unauthorized` before any file handling logic runs.

---

## Sample Requests and Responses

### Upload Profile Photo

**Request**

```bash
curl -X POST "https://api.example.com/api/v1/users/me/profile-photo" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -F "file=@avatar.png"
```

**Response `200 OK`**

```json
{
  "message": "Profile photo updated",
  "path": "uploads/profile_photos/42/9f1c2b3a4d5e6f7a8b9c0d1e2f3a4b5c.png"
}
```

### Upload Document

**Request**

```bash
curl -X POST "https://api.example.com/api/v1/documents" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -F "file=@contract.pdf"
```

**Response `201 Created`**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "user_id": 42,
  "original_filename": "contract.pdf",
  "stored_filename": "a1b2c3d4e5f6.pdf",
  "file_path": "uploads/documents/42/a1b2c3d4e5f6.pdf",
  "file_type": "application/pdf",
  "file_size": 184320,
  "uploaded_at": "2026-08-31T10:15:00Z",
  "is_deleted": false
}
```

### List Documents

**Request**

```bash
curl -X GET "https://api.example.com/api/v1/documents" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Response `200 OK`**

```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "original_filename": "contract.pdf",
    "file_type": "application/pdf",
    "file_size": 184320,
    "uploaded_at": "2026-08-31T10:15:00Z"
  }
]
```

### Delete Document

**Request**

```bash
curl -X DELETE "https://api.example.com/api/v1/documents/3fa85f64-5717-4562-b3fc-2c963f66afa6" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Response `204 No Content`**

### Error Example — Invalid File Type

```json
{
  "detail": "File type application/x-msdownload not allowed"
}
```

### Error Example — Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

---

## Security Considerations

- **Never trust client-supplied filenames or MIME types.** Always verify with magic-byte inspection (`python-magic`) in addition to extension/content-type checks.
- **Randomize stored filenames** (UUIDs) to prevent path traversal and enumeration attacks.
- **Enforce size limits at multiple layers**: reverse proxy (e.g., Nginx `client_max_body_size`), application logic, and — for object storage — provider-side limits.
- **Store uploads outside the web root**, or in object storage (S3/GCS) with signed, time-limited URLs rather than serving files directly from a public static folder.
- **Scan uploads for malware** where feasible (e.g., ClamAV) before making files available for download, especially for document types like `.docx`/`.xls` that can carry macros.
- **Enforce per-user ownership checks** on every read/delete operation; return `404` rather than `403` for resources belonging to other users to avoid leaking existence.
- **Use soft deletes** for documents to support audit trails and recovery, and purge underlying files via a scheduled job rather than inline in the request path.
- **Rate-limit upload endpoints** to prevent storage-exhaustion or denial-of-service via repeated large uploads.
- **Set short JWT expiry** with refresh tokens, and validate `exp`, `iat`, and signature on every request; store the signing secret in environment variables / a secrets manager, never in source control.
- **Disable execution permissions** on the upload directory so uploaded files (e.g., disguised scripts) cannot be executed by the server.
- **Sanitize and validate image files** (e.g., re-encode images server-side) to strip potentially malicious embedded metadata or payloads.
- **Log upload/delete actions** with user ID, timestamp, and file hash for auditability, without logging file contents.