from pydantic import BaseModel, ConfigDict


class child_document(BaseModel):
    child_id: int
    orignal_name: str
    stored_name: str
    file_path: str
    file_type: str
    uploaded_by: int

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    u_id: int
    u_name: str
    email: str
    u_role: str

class childbase(BaseModel):
    c_id: int
    c_name: str
    age_months: int
    gender: str
    weight_kg: float
    height_cm: float
    district_id: int
    health_worker_id: int
    

class Childcreate(childbase):
    profile_photo: str

class childresponse(childbase):

    model_config = ConfigDict(from_attributes=True)