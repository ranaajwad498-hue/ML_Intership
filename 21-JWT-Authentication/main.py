from fastapi import Depends, FastAPI, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from auth import verify_token, get_db
from database import base, engine
from model import User, children, prediction
from schemas import (
    TokenResponse, UserCreate, UserLogin, UserResponse, 
    ChildResponse, ChildBase, ChildUpdate, PredictionRequest, predictionresponse
)
from services import AuthService
from fastapi.security import OAuth2PasswordRequestForm

base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication System")

@app.get("/")
def read_root():
    return {
            "status": "online", 
            "message": "Welcome to the Authentication System API"}

@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.create_user(user_data=user_data, db=db)


@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    user = AuthService.authenticate_user(user_data=user_data, db=db)

    access_token = AuthService.create_access_token(
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


@app.get("/auth/me", response_model=UserResponse)
def auth_me(token: Optional[str] = Query(None, description="Raw JWT token string"),db: Session = Depends(get_db)):
    if token:
        return verify_token(token=token, db=db)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated. Provide a Bearer token or ?token= parameter.",
        headers={"WWW-Authenticate": "Bearer"},
    )



@app.get("/children", response_model=List[ChildResponse])
def view_children(current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if current_user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    return db.query(children).all()


@app.post("/add_child", response_model=ChildResponse)
def add_child(child: ChildBase, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if current_user.u_role not in {"Admin", "Worker", "Health Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    
    assigned_id = child.health_worker_id
    if current_user.u_role in {"Worker", "Health Worker"}:
        assigned_id = current_user.u_id

    new_child = children(
        c_name=child.c_name,
        age_months=child.age_months,
        gender=child.gender,
        weight_kg=child.weight_kg,
        height_cm=child.height_cm,
        district_id=child.district_id,
        health_worker_id=assigned_id
    )
    db.add(new_child)
    db.commit()
    db.refresh(new_child)
    return new_child


@app.put("/children/{child_id}", response_model=ChildResponse)
def update_child(child_id: int, child_data: ChildUpdate, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    db_child = db.query(children).filter(children.c_id == child_id).first()
    
    if not db_child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child Record not Found"
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

    update_dict = child_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_child, key, value)

    db.commit()
    db.refresh(db_child)
    return db_child


@app.delete("/children/{child_id}")
def del_child(child_id: int, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if current_user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Access only"
        )

    db_child = db.query(children).filter(children.c_id == child_id).first()
    
    if not db_child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child record not found"
        )

    db.delete(db_child)
    db.commit()
    return {
        "message": f"Child Record with id {child_id} is deleted successfully"
    }


@app.post("/prediction", response_model=predictionresponse)
def request_prediction(payload: PredictionRequest, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if current_user.u_role not in {"Worker", "Health Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Health Workers can request ML predictions"
        )
    
    db_child = db.query(children).filter(children.c_id == payload.child_id).first()
    if not db_child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Child record not found"
        )

    # Instantiate prediction with all non-nullable values
    new_prediction = prediction(
        child_id=payload.child_id,
        requested_by=current_user.u_id,
        risk_score=0.15,
        risk_catgory="Low",
        confidence="95%",
        reasons="Healthy growth parameters",
        model_name="NourishPak-v1"
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction


@app.get("/admin/prediction", response_model=List[predictionresponse])
def view_prediction(current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if current_user.u_role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return db.query(prediction).all()


@app.get("/admin/users", response_model=List[UserResponse])
def manage_users(current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if current_user.u_role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return db.query(User).all()