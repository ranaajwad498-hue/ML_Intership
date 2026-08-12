from typing import List, Dict
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

class Child(BaseModel):
    child_id: int = Field(..., gt=0, description="child_id must be greater than 0")
    name: str = Field(..., min_length=1, description="name must not be empty")
    age_months: int = Field(..., ge=0, description="age_months must not be negative")
    gender: str = Field(..., min_length=1, description="Gender (e.g., Male, Female)")
    weight_kg: float = Field(..., gt=0, description="weight_kg must be greater than 0")
    height_cm: float = Field(..., gt=0, description="height_cm must be greater than 0")

 
class ChildService:
    def __init__(self):
        self._children: Dict[int, Child] = {}
 
    def add_child(self, child: Child) -> Child:
        if child.child_id in self._children:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Child with ID {child.child_id} already exists.")
        self._children[child.child_id] = child
        return child

    def get_all_children(self) -> List[Child]:
        return list(self._children.values())

    def get_child(self, child_id: int) -> Child:
        if child_id not in self._children:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child not found")
        return self._children[child_id]

    def update_child(self, child_id: int, updated_child: Child) -> Child:
        if child_id not in self._children:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child not found")
        self._children[child_id] = updated_child
        return updated_child

    def delete_child(self, child_id: int) -> int:
        if child_id not in self._children:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child not found" )
        del self._children[child_id]
        return child_id


app = FastAPI()
child_service = ChildService()


@app.post("/children", status_code=status.HTTP_201_CREATED)
def add_child(child: Child):
    added_child = child_service.add_child(child)
    return {
        "message": "Child Added Successfully",
        "child_id": added_child.child_id
    }

@app.get("/children", response_model=List[Child], status_code=status.HTTP_200_OK)
def get_all_children():
    return child_service.get_all_children()

@app.get("/children/{child_id}", response_model=Child, status_code=status.HTTP_200_OK)
def get_child(child_id: int):
    return child_service.get_child(child_id)


@app.put("/children/{child_id}", status_code=status.HTTP_200_OK)
def update_child(child_id: int, child: Child):
    child_service.update_child(child_id, child)
    return {
        "message": "Child Updated Successfully",
        "child_id": child_id
    }


@app.delete("/children/{child_id}", status_code=status.HTTP_200_OK)
def delete_child(child_id: int):
    child_service.delete_child(child_id)
    return {
        "message": "Child Deleted Successfully",
        "child_id": child_id
    }

  