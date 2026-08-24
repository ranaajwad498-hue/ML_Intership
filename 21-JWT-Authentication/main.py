from database import base, engine, session
from fastapi import Depends, FastAPI, status
from auth import verify_password, verify_token
from schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from services import AuthService
from sqlalchemy.orm import Session

base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication System")

def get_db():
    db= session()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.create_user(user_data=user_data, db=db)


@app.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(user_data=user_data, db=db)

    access_token = AuthService.create_access_token(
        data={"sub": str(user.u_id)}
    )

    return TokenResponse(
        message="Login Sucessfuly",
        access_token=access_token,
        token_type="bearer",
        u_role=user.u_role,
    )


@app.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(verify_token)):

    return current_user {
        "message": "Authenticated successfully",
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"],}


@app.get("/role-check")
def check_user_role(
    current_user_id: int = Depends(verify_password), db: Session = Depends(get_db)
):
    user = AuthService.get_current_user(id=current_user_id, db=db)
    return AuthService.check_role(user)