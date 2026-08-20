from typing import Optional
from pydantic import BaseModel, ConfigDict

class ChildBase(BaseModel):
    c_id:int
    c_name: str
    age_months: int
    gender: str
    weight_kg: float
    height_cm: float
    district_id: int
    health_worker_id: int

class ChildCreate(ChildBase):
    c_id: int 

class ChildUpdate(BaseModel):
    c_id:int
    c_name: Optional[str] = None
    age_months: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    district_id: Optional[int] = None
    health_worker_id: Optional[int] = None

class ChildResponse(ChildBase):
    c_id: int

    model_config = ConfigDict(from_attributes=True)