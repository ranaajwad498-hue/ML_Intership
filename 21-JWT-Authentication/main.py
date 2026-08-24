from fastapi import Depends, FastAPI, status, Header, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from auth import verify_token
from database import base, engine, session
from model import User
from schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from services import AuthService

base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication System")


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.create_user(user_data=user_data, db=db)


@app.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(user_data=user_data, db=db)

    access_token = AuthService.create_access_token(
        user_id=user.u_id, email=user.email, role=user.u_role
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        u_id=user.u_id,
        u_name=user.u_name,
        email= user.email,
        u_role=user.u_role,
    )


@app.get("/auth/me", response_model=UserResponse)
def auth_me(token: Optional[str] = Query(None, description="Raw JWT token string"),db: Session = Depends(get_db)):
    if token:
        return verify_token(token=token, db=db)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated. Provide a Bearer token or ?token= parameter.",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.post("/admin/dashboard")
def admin_dashboard(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(user_data=user_data, db=db)
    if user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot Access",
        )

    return {
        "message": "Welcome Admin",
        "Role": user.u_role,
    }
    

@app.post("/worker/dashboard")
def health_worker_dashboard(user_data:UserLogin, db:Session=Depends(get_db)):
    user = AuthService.authenticate_user(user_data=user_data, db=db)
    if user.email == "worker@gmail.com":
        return{
            "message": "Welcome Health Worker",
            "Role": user.u_role,
        }


 
