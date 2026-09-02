from sqlalchemy import Column, Integer, Float, String, DateTime
from database import base
from sqlalchemy import func


class ChildPredictionRequest(base):
    __tablename__ = "ChildPredictionRequest"

    child_id=   Column(Integer, primary_key=True, autoincrement=True)
    age_months= Column(Float, nullable=False, index= True)
    gender=     Column(String, nullable= False, index= True)
    mother_education= Column(String, nullable=False, index=True)
    household_wealth_index= Column(String, nullable=False, index=True)
    weight_kg=  Column(Float, nullable=False, index= True)
    height_cm=  Column(Float, nullable=False, index= True)


class User(base):
    __tablename__ = "users"

    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    u_role = Column(String, nullable=False, default="Worker")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
