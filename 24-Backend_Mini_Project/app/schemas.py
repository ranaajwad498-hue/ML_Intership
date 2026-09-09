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