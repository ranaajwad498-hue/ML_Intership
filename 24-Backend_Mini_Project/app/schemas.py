from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional,List
from datetime import datetime

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
    child_id: int = Field(..., gt=0, example=101)
    age_months: float = Field(..., ge=0, example=18.0)
    gender: Literal["Male", "Female"]
    mother_education: Literal["No education", "Primary", "Secondary", "Higher"] = Field(
        "Secondary", example="Secondary"
    )
    household_wealth_index: Literal["Poorest", "Poor", "Middle", "Richer", "Richest"] = Field(
        "Middle", example="Middle"
    )
    weight_kg: float = Field(..., gt=0, example=7.8)
    height_cm: float = Field(..., gt=0, example=74.0)
    health_worker_id: int
    profile_photo: Optional[str] = None

class ChildUpdate(BaseModel):
    c_name: Optional[str] = None
    age_months: Optional[int] = None
    gender: Optional[str] = None
    mother_education:Optional[str]=None
    household_wealth_education:Optional[str]=None
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


class ChildPredictionRequest(BaseModel):
    child_id: int = Field(..., gt=0, example=101)
    age_months: float = Field(..., ge=0, example=18.0)
    gender: Literal["Male", "Female"]
    mother_education: Literal["No education", "Primary", "Secondary", "Higher"] = Field(
        "Secondary", example="Secondary"
    )
    household_wealth_index: Literal["Poorest", "Poor", "Middle", "Richer", "Richest"] = Field(
        "Middle", example="Middle"
    )
    weight_kg: float = Field(..., gt=0, example=7.8)
    height_cm: float = Field(..., gt=0, example=74.0)


class PredictionResponse(BaseModel):
    p_id: int
    child_id: int
    risk_score: int
    category: str
    confidence: float
    advice: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionHistoryItem(BaseModel):
    risk_score: int
    category: str
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionHistoryResponse(BaseModel):
    child_id: int
    total_predictions: int
    predictions: List[PredictionHistoryItem]

class DirectPredictionRequest(BaseModel):
    age_months: float = Field(..., ge=0, example=18.0)
    gender: Literal["Male", "Female"]
    mother_education: Literal["No education", "Primary", "Secondary", "Higher"] = Field(
        "Secondary", example="Secondary"
    )
    household_wealth_index: Literal["Poorest", "Poor", "Middle", "Richer", "Richest"] = Field(
        "Middle", example="Middle"
    )
    weight_kg: float = Field(..., gt=0, example=7.8)
    height_cm: float = Field(..., gt=0, example=74.0)

class DirectPredictionResponse(BaseModel):
    risk_score: int
    category: str
    confidence: float
    advice: str
    model_config = ConfigDict(from_attributes=True)

