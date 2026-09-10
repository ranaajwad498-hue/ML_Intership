from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class userCreate(BaseModel):
    u_name: str
    email: str
    password: str
    u_role: Optional[str] = "Health_worker"

class userlogin(BaseModel):
    email: str
    password: str

class tokenresponse(BaseModel):
    access_token: str
    token_type: str
    u_id: int
    u_name: str
    email: str
    u_role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class ChildCreate(BaseModel):
    c_name: str
    age_months: int
    gender: str
    weight_kg: float
    height_cm: float
    district_id: int
    health_worker_id: int
    profile_photo: Optional[str] = None

class ChildUpdate(BaseModel):
    c_name: Optional[str] = None
    age_months: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    district_id: Optional[int] = None
    health_worker_id: Optional[int] = None
    profile_photo: Optional[str] = None

class ChildResponse(ChildCreate):
    c_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)