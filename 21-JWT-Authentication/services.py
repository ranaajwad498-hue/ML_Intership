from datetime import datetime, timedelta, timezone
from auth import hash_password, verify_password
from fastapi import HTTPException, status
import jwt
from model import User
from schemas import UserCreate, UserLogin
from sqlalchemy.orm import Session

SECRET_KEY = "ajwad321"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:

    @staticmethod
    def create_user(user_data: UserCreate, db: Session):
        existing_user = (
            db.query(User).filter(User.email == user_data.email).first()
        )
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
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )

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
    def check_role(user: User):
        if user.u_role == "Admin":
            return {"message": "Welcome Admin", "role": "Admin"}
        else:
            return {"message": "Welcome Worker", "role": user.u_role}