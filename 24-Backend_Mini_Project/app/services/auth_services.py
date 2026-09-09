from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import userCreate, userlogin
from app.auth import authentication
from app.models import users

class auth_services():

    @staticmethod
    def create_user(db: Session, user: userCreate):
        hashed_password = authentication.hashpassword(user.password)
        db_user = users(
            u_name=user.u_name,
            email=user.email,
            password=hashed_password,
            u_role=user.u_role or "Health_worker"
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(user_data: userlogin, db: Session):
        db_user = db.query(users).filter(users.email == user_data.email).first()
        if not db_user or not authentication.verify_password(user_data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Email or Password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return db_user