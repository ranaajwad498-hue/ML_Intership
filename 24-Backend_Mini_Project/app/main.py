from app.database import base, engine
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from app.services.auth_services import auth_services
from app.schemas import tokenresponse, userCreate, userlogin, ChildCreate,ChildResponse,ChildUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authentication, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from app.models import users,child
from app.services.child_services import child_services

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

@app.post("/children/")
def create_child(child_data: ChildCreate, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    new_child= child_services.create_child(db=db, child_data=child_data)
    if current_user.u_role == "Health_worker":
        child_data.health_worker_id = current_user.u_id
    return {
        "message": "Child Added Successfully",
        "child_id": new_child.c_id

    }
@app.get("/children/", response_model=list[ChildResponse])
def get_all_children(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    return child_services.get_all_children(db=db, skip=skip, limit=limit) 

@app.get("/children/{c_id}", response_model=ChildResponse)
def get_single_child(c_id: int, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    return child_services.get_child_by_id(db=db, c_id=c_id)

@app.put("/children/{c_id}")
def update_child(c_id: int, child_data: ChildUpdate, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    child_update=child_services.update_child(db=db, c_id=c_id, child_data=child_data)
    return {
        "message": "Child Updated Successfully",
        "child_id": child_update.c_id
        }

@app.delete("/children/{c_id}")
def delete_child(c_id: int, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    return child_services.delete_child(db=db, c_id=c_id)

@app.get("/children")
def children_count(db:Session=Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    total_count=child_services.get_total_children(db=db)
    return{
        "Total Children": total_count
    }