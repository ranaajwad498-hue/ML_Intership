from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import child,prediction
from app.schemas import ChildCreate, ChildUpdate

class child_services:

    @staticmethod
    def create_child(db: Session, child_data: ChildCreate):
        db_child = child(**child_data.model_dump())
        db.add(db_child)
        db.commit()
        db.refresh(db_child)
        return db_child

    @staticmethod
    def get_all_children(db: Session, skip: int = 0, limit: int = 100):
        return db.query(child).offset(skip).limit(limit).all()

    @staticmethod
    def get_child_by_id(db: Session, c_id: int):
        db_child = db.query(child).filter(child.c_id == c_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found"
            )
        return db_child

    @staticmethod
    def update_child(db: Session, c_id: int, child_data: ChildUpdate):
        db_child = child_services.get_child_by_id(db, c_id)
        if not db_child:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Child Not Found"
            )
        update_data = child_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_child, key, value)
        db.commit()
        db.refresh(db_child)
        return db_child

    @staticmethod
    def delete_child(db: Session, c_id: int):
        db_child = child_services.get_child_by_id(db, c_id)
        db.query(prediction).filter(prediction.child_id == c_id).delete()
        if not db_child:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Child Not Found"
            )
        db.delete(db_child)
        db.commit()
        return {"detail": "Child deleted successfully"}
    
    def get_total_children(db: Session):
        return db.query(child).count()