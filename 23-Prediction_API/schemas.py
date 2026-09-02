from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, List
from datetime import datetime


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


class userlogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    u_id: int
    u_name: str
    email: str
    u_role: str