from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class childbase(BaseModel):
    age_months:float= Field(gt=0)
    gender:Literal["Male", "Femlae"]
    mother_education:Literal["No education", "Primary", "Secondary", "Higher"]
    household_wealth_index:Literal["Low", "Middle", "High"]
    weight_kg:float = Field(gt=0)
    height_cm:float = Field(gt=0)

class childpredict(childbase):
    child_id:int


class prediction_response(childbase):
    model_config= ConfigDict(from_attributes=True)

class user(BaseModel):
    email:str
    password:str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    u_id: int
    u_name: str
    email: str
    u_role: str
