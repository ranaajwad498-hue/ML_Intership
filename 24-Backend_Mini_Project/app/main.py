from app.database import base, engine
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from app.services.auth_services import auth_services
from app.schemas import tokenresponse, userCreate, userlogin
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authentication, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from app.models import users

base.metadata.create_all(bind=engine)

app = FastAPI(title="Child CRUD API")


@app.post("/sign_up", response_model=tokenresponse)
def sign_up(user: userCreate, db: Session = Depends(get_db)):
    existing_user = db.query(users).filter(users.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Already Exists"
        )
    created_user = auth_services.create_user(db=db, user=user)
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"user_id": created_user.u_id, "sub": created_user.u_name, "role": created_user.u_role},
        expires_delta=access_token_expire
    )
    return tokenresponse(
        access_token=access_token,
        token_type="bearer",
        u_id=created_user.u_id,
        u_name=created_user.u_name,
        email=created_user.email,
        u_role=created_user.u_role,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at
    )

@app.post("/login", response_model=tokenresponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    userdata = userlogin(email=form_data.username, password=form_data.password)
    user = auth_services.authenticate_user(user_data=userdata, db=db)
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"user_id": user.u_id, "sub": user.u_name, "role": user.u_role},
        expires_delta=access_token_expire
    )
    return tokenresponse(
        access_token=access_token,
        token_type="bearer",
        u_id=user.u_id,
        u_name=user.u_name,
        email=user.email,
        u_role=user.u_role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )