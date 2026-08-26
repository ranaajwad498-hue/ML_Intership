from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    u_name: str
    u_role: Optional[str] = "Worker"
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    u_id: int
    u_name: str
    email: str
    u_role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    u_id: int
    u_name: str
    email: str
    u_role: str


class ChildBase(BaseModel):
    c_name: str
    age_months: int
    gender: str
    weight_kg: float
    height_cm: float
    district_id: Optional[int] = None
    health_worker_id: Optional[int] = None


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
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


class PredictionRequest(BaseModel):
    child_id: int


class viewpredction(BaseModel):
    p_id: int
    child_id: int
    risk_score: float
    risk_catgory: str
    confidence: str
    reasons: str
    model_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class predictionresponse(viewpredction):
    pass