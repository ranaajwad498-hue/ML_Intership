from datetime import datetime, timedelta, timezone
from auth import (
    hash_password, 
    verify_password, 
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES)
from fastapi import HTTPException, status
import jwt
from model import User, children, prediction
from schemas import UserCreate, UserLogin, ChildUpdate
from sqlalchemy.orm import Session
from typing import List


class AuthService:

    @staticmethod
    def create_user(user_data: UserCreate, db: Session):
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_pwd = hash_password(user_data.password)
        db_user = User(
            u_name=user_data.u_name,
            email=user_data.email,
            password=hashed_pwd,
            u_role=user_data.u_role or "Worker",
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

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
    def create_access_token(user_id: int, email: str, role: str, expires_delta: timedelta = None) -> str:
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

    @staticmethod
    def get_current_user(id: int, db: Session):
        db_user = db.query(User).filter(User.u_id == id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    @staticmethod
    def get_all_children(db: Session, skip: int = 0, limit: int = 100) -> List[children]:
        return db.query(children).offset(skip).limit(limit).all()

    @staticmethod
    def get_child_by_id(child_id: int, db: Session):
        db_child = db.query(children).filter(children.c_id == child_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Child record with ID {child_id} not found.",
            )
        return db_child

    @staticmethod
    def update_child(child_id: int, update_child: ChildUpdate, db: Session):
        db_child = AuthService.get_child_by_id(child_id, db)
        update_data = update_child.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_child, key, value)

        db.commit()
        db.refresh(db_child)
        return db_child

    @staticmethod
    def delete_child(child_id: int, db: Session):
        db_child = AuthService.get_child_by_id(child_id, db)
        db.delete(db_child)
        db.commit()
        return {
            "message": f"Child Record with ID {child_id} deleted successfully"
        }

    @staticmethod
    def view_prediction(db: Session, skip: int = 0, limit: int = 100) -> List[prediction]:
        return db.query(prediction).offset(skip).limit(limit).all()