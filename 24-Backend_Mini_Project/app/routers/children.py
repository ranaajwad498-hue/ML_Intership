from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import ChildCreate,ChildResponse,ChildUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authentication
from app.models import users,child
from app.services.child_services import child_services

router = APIRouter()


@router.post("/children/")
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
@router.get("/children/", response_model=list[ChildResponse])
def get_all_children(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    return child_services.get_all_children(db=db, skip=skip, limit=limit) 

@router.get("/children/{c_id}", response_model=ChildResponse)
def get_single_child(c_id: int, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    return child_services.get_child_by_id(db=db, c_id=c_id)

@router.put("/children/{c_id}")
def update_child(c_id: int, child_data: ChildUpdate, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    db_child=db.query(child).filter(child.c_id == c_id).first()
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    
    if not db_child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child Record not Found"
        )

    if current_user.u_role =="Health_worker" and db_child.health_worker_id != current_user.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )

    child_update=child_services.update_child(db=db, c_id=c_id, child_data=child_data)
    return {
        "message": "Child Updated Successfully",
        "child_id": child_update.c_id
        }

@router.delete("/children/{c_id}")
def delete_child(c_id: int, db: Session = Depends(get_db), current_user: users = Depends(authentication.verify_token)):
    db_child=db.query(child).filter(child.c_id == c_id).first()

    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        )
    if not db_child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child Record not Found"
        )

    if current_user.u_role =="Health_worker" and db_child.health_worker_id != current_user.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denined"
        ) 

    return child_services.delete_child(db=db, c_id=c_id)

@router.get("/children/count")
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