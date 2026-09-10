from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Float
from app.database import base
from sqlalchemy import func

class users(base):
    __tablename__ = "users"

    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    u_role = Column(String, nullable=False, default="Worker")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class child(base):
    __tablename__ = "child"

    c_id = Column(Integer, primary_key=True, index=True)
    c_name = Column(String, nullable=False, index=True)
    age_months = Column(Integer, nullable=False, index=True)
    gender = Column(String, nullable=False, index=True)
    weight_kg = Column(Float, nullable=False, index=True)
    height_cm = Column(Float, nullable=False, index=True)
    district_id = Column(BigInteger, nullable=False, index=True)
    health_worker_id = Column(BigInteger, nullable=False, index=True)
    profile_photo = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class districts(base):
    __tablename__="districts"

    d_id= Column(Integer, primary_key=True, index=True)
    d_name= Column(String, nullable=False, index=True)
    province= Column(String, nullable=False, index=True)
    created_at= Column(DateTime(timezone=True), server_default=func.now())

class health_worker(base):
    __tablename__= "health_worker"

    h_id= Column(Integer, primary_key=True, index= True)
    user_id= Column(Integer, ForeignKey("users.u_id"))
    district_id= Column(Integer, ForeignKey("districts.d_id"))
    phone= Column(BigInteger, nullable=False, index=False)
    desgination= Column(String, nullable=False, index=True)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    updated_at= Column(DateTime(timezone=True),onupdate=func.now(), server_default=func.now())

class prediction(base):
    __tablename__="prediction"

    p_id=Column(Integer, primary_key=True, autoincrement=True, index=True)
    child_id= Column(Integer, ForeignKey("child.c_id"))
    risk_score= Column(Integer, nullable=False, index=True)
    risk_catagory= Column(String, nullable=False, index=True)
    confidence= Column(String, nullable=False, index=True)
    model_name= Column(String, nullable=False, index=True)
    advice= Column(String, nullable=False, index=True)
    created_at= Column(DateTime(timezone=True), server_default=func.now())