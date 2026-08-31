import os
import uuid
import magic
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from schmas import UserLogin
from models import User, Children, child_documents
from sqlalchemy.orm import Session
from typing import Optional
from auth import (
    verify_password, 
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".txt", ".docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_FILE_SIZE_MB = 5.0
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

PROFILE_DIR = "uploads/profile_photos"
DOCUMENTS_DIR = "uploads/documents"

def generate_unique_filename(child_id: int, original_filename: str) -> str:
    base_name, ext = os.path.splitext(original_filename or "file")
    clean_base_name = "".join(
        c for c in base_name if c.isalnum() or c in ("-", "_")
    ).strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]

    return f"child_{child_id}_{timestamp}_{unique_id}_{clean_base_name}{ext.lower()}"

class ChildFileService:
    PROFILE_DIR = PROFILE_DIR
    DOCUMENTS_DIR = DOCUMENTS_DIR

    @staticmethod
    def generate_secure_filename(child_id: int, file: UploadFile) -> str:
        return generate_unique_filename(child_id, file.filename or "file")

    @staticmethod
    async def validate_file(file: UploadFile, max_mb: float = MAX_FILE_SIZE_MB):
        _, ext = os.path.splitext(file.filename or "")
        ext = ext.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extension '{ext}' is not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        content = await file.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty."
            )

        max_bytes = max_mb * 1024 * 1024
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {max_mb} MB."
            )

        detected_mime = magic.from_buffer(content, mime=True)
        if detected_mime not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File content signature ('{detected_mime}') does not match allowed file types."
            )
        await file.seek(0)

    @classmethod
    async def save_profile_photo(cls, child_id: int, uploaded_by_id: int, file: UploadFile, db: Session) -> str:
        os.makedirs(cls.PROFILE_DIR, exist_ok=True)
        await cls.validate_file(file)
        db_child = db.query(Children).filter(Children.c_id == child_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Child not found"
            )

        unique_filename = cls.generate_secure_filename(
            child_id=child_id, file=file
        )
        file_path = os.path.join(cls.PROFILE_DIR, unique_filename).replace(
            "\\", "/"
        )
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        db_child.profile_photo = file_path
        new_photo = child_documents(
            child_id=child_id,
            original_name=file.filename,
            stored_name=unique_filename,
            file_path=file_path,
            file_type=file.content_type or "application/octet-stream",
            uploaded_by=uploaded_by_id,
        ) 
        db.add(new_photo)
        db.commit()
        db.refresh(db_child)
        return file_path

    @classmethod
    async def save_child_document(cls, child_id: int, uploaded_by_id: int, file: UploadFile, db: Session) -> child_documents:
        os.makedirs(cls.DOCUMENTS_DIR, exist_ok=True)
        await cls.validate_file(file)
        db_child = db.query(Children).filter(Children.c_id == child_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Child not found"
            )

        unique_filename = cls.generate_secure_filename(
            child_id=child_id, file=file
        )
        file_path = os.path.join(cls.DOCUMENTS_DIR, unique_filename).replace("\\", "/")
    
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        new_doc = child_documents(
            child_id=child_id,
            original_name=file.filename,
            stored_name=unique_filename,
            file_path=file_path,
            file_type=file.content_type or "application/octet-stream",
            uploaded_by=uploaded_by_id,
        ) 
        db.add(new_doc)
        db.commit()
        return new_doc

    @classmethod
    def get_child_documents(cls, filename: str) -> FileResponse:
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(cls.DOCUMENTS_DIR, safe_filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{safe_filename}' not found."
            )

        return FileResponse(
            path=file_path,
            filename=safe_filename,
            media_type="application/octet-stream"
        )

    @classmethod
    def delete_document(cls, filename: str) -> dict:
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(cls.DOCUMENTS_DIR, safe_filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{safe_filename}' not found."
            )
        os.remove(file_path)
        return {"detail": f"Document '{safe_filename}' deleted successfully."}

    @classmethod
    async def update_profile_photo(
        cls, child_id: int, file: UploadFile, db: Session
    ) -> str:
        await cls.validate_file(file)
        db_child = db.query(Children).filter(Children.c_id == child_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Child with ID {child_id} not found",
            )
        old_photo_path = db_child.profile_photo
        if old_photo_path and os.path.exists(old_photo_path):
            try:
                os.remove(old_photo_path)
            except OSError:
                pass
        os.makedirs(cls.PROFILE_DIR, exist_ok=True)
        unique_filename = cls.generate_secure_filename(
            child_id=child_id, file=file
        )
        new_file_path = os.path.join(cls.PROFILE_DIR, unique_filename).replace(
            "\\", "/"
        )

        content = await file.read()
        with open(new_file_path, "wb") as f:
            f.write(content)
        db_child.profile_photo = new_file_path
        db.commit()
        db.refresh(db_child)

        return new_file_path

    @staticmethod
    def authenticate_user(user_data: UserLogin, db: Session):
        user = db.query(User).filter(User.email == user_data.email).first()

        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Email or Password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    @staticmethod
    def create_access_token(user_id: int, email: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "sub": str(user_id),  
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": expire,
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)