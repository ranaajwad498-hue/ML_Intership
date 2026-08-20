from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Child
from schemas import ChildCreate, ChildResponse, ChildUpdate


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChildService:

    @staticmethod
    def create_child(child_data: ChildCreate, db: Session) -> Child:
        db_child = Child(**child_data.model_dump())
        db.add(db_child)
        db.commit()
        db.refresh(db_child)
        return db_child

    @staticmethod
    def get_child_by_id(child_id: int, db: Session) -> Child:
        db_child = db.query(Child).filter(Child.c_id == child_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Child record with ID {child_id} not found.",
            )
        return db_child

    @staticmethod
    def get_all_children(db: Session, skip: int = 0, limit: int = 100) -> List[Child]:
        return db.query(Child).offset(skip).limit(limit).all()

    @staticmethod
    def update_child(child_id: int, child_data: ChildUpdate, db: Session) -> Child:
        db_child = ChildService.get_child_by_id(child_id, db)
        update_data = child_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_child, key, value)

        db.commit()
        db.refresh(db_child)
        return db_child

    @staticmethod
    def delete_child(child_id: int, db: Session) -> dict:
        db_child = ChildService.get_child_by_id(child_id, db)
        db.delete(db_child)
        db.commit()
        return {"message": f"Child record with ID {child_id} deleted successfully."}


app = FastAPI(title="NourishPak Child Care API")
child_service = ChildService()


@app.get("/")
def read_root():
    return {"message": "Child CRUD Operations Active"}


@app.post("/children", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
def create_child_record(child: ChildCreate, db: Session = Depends(get_db)):
    return child_service.create_child(child_data=child, db=db)


@app.get("/children/{child_id}", response_model=ChildResponse)
def get_child_record(child_id: int, db: Session = Depends(get_db)):
    return child_service.get_child_by_id(child_id=child_id, db=db)


@app.get("/children", response_model=List[ChildResponse])
def list_children_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return child_service.get_all_children(db=db, skip=skip, limit=limit)


@app.patch("/children/{child_id}", response_model=ChildResponse)
def update_child_record(child_id: int, child: ChildUpdate, db: Session = Depends(get_db)):
    return child_service.update_child(child_id=child_id, child_data=child, db=db)


@app.delete("/children/{child_id}", status_code=status.HTTP_200_OK)
def delete_child_record(child_id: int, db: Session = Depends(get_db)):
    return child_service.delete_child(child_id=child_id, db=db)