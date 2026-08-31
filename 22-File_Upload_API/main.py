import os
from typing import Annotated
from fastapi import FastAPI, Depends, UploadFile, File, status, HTTPException
from schmas import UserLogin, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import get_db, verify_token
from file_services import ChildFileService
from models import Children, User 
from fastapi.responses import FileResponse

app = FastAPI()

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
IMAGE_MIMES = {"image/jpeg", "image/png", "image/webp"}

DOC_EXTS = {".pdf", ".docx", ".doc", ".txt"}

@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    user = ChildFileService.authenticate_user(user_data=user_data, db=db)

    access_token = ChildFileService.create_access_token(
        user_id=user.u_id, email=user.email, role=user.u_role
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        u_id=user.u_id,
        u_name=user.u_name,
        email=user.email,
        u_role=user.u_role,
    )

@app.post("/children/{child_id}/photos", status_code=status.HTTP_201_CREATED)
async def upload_child_file(child_id: int, file: Annotated[UploadFile, File(...)], db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    if current_user.u_role not in {"Admin", "Worker", "Health Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )    
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower()
    content_type = file.content_type.lower() if file.content_type else ""
    if ext in IMAGE_EXTS or content_type in IMAGE_MIMES:
        saved_path = await ChildFileService.save_profile_photo(
            child_id=child_id,
            uploaded_by_id=current_user.u_id,
            file=file,
            db=db,
        )

    elif ext in DOC_EXTS:
        saved_path = await ChildFileService.save_child_document(
            child_id=child_id,
            uploaded_by_id=current_user.u_id,
            file=file,
            db=db,
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file format '{ext}'. Please upload a valid image or document.",
        )

    return {
        "message": "File processed and saved successfully",
        "child_id": child_id,
        "filename": file.filename,
        "saved_path": saved_path,
    }

@app.get("/children/{child_id}/file")
def get_child_file(child_id: int, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    db_child = db.query(Children).filter(Children.c_id == child_id).first()
    
    if not db_child:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Children Record with {child_id} not Found"
        )
        
    if current_user.u_role not in {"Admin", "Worker", "Health Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    
    if current_user.u_role in {"Worker", "Health Worker"} and db_child.health_worker_id != current_user.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have Access"
        )

    file_path = db_child.profile_photo
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File path does not exist on server",
        )

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/octet-stream",
    )

@app.put("/children/{child_id}/profile-photo", status_code=status.HTTP_200_OK)
async def update_child_profile_photo(
    child_id: int,
    file: Annotated[UploadFile, File(...)],
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    if current_user.u_role not in {"Admin", "Worker", "Health Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    db_child = db.query(Children).filter(Children.c_id == child_id).first()

    if not db_child:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Children Record with {child_id} not Found"
        )
    
    if current_user.u_role in {"Worker", "Health Worker"} and db_child.health_worker_id != current_user.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have Access"
        )
    
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower()
    content_type = file.content_type.lower() if file.content_type else ""
    if ext in IMAGE_EXTS or content_type in IMAGE_MIMES:
        saved_path = await ChildFileService.update_profile_photo(
            child_id=child_id,
            file=file,
            db=db,
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file format '{ext}'. Please upload a valid image.",
        )
    
    return {
        "message": "Profile photo updated successfully",
        "child_id": child_id,
        "profile_photo": saved_path,
    }

@app.delete("/children/{child_id}/file")
def delete_child(child_id: int, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    db_child = db.query(Children).filter(Children.c_id == child_id).first()

    if not db_child:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Children Record with {child_id} not Found"
        )

    if current_user.u_role not in {"Admin", "Worker", "Health Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    
    if current_user.u_role in {"Worker", "Health Worker"} and db_child.health_worker_id != current_user.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have Access"
        )

    file_path = db_child.profile_photo
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File path does not exist on server",
        )
    db.delete(db_child)
    db.commit()
    return {
        "message": "Document Deleted Successfully",
        "document_id": f"{child_id}"
    }