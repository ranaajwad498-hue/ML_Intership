from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = "users"

    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    u_role = Column(String, nullable=False, default="Worker")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class HealthWorker(base):
    __tablename__ = 'health_worker'

    h_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.u_id"))
    district_id = Column(Integer, ForeignKey("districts.d_id"))
    phone = Column(String(20))
    desgination = Column(String(255)) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class District(base):
    __tablename__ = 'districts'

    d_id = Column(Integer, primary_key=True, autoincrement=True)
    d_name = Column(String(255))
    province = Column(String(255))
    create_at = Column(DateTime(timezone=True), server_default=func.now())


class children(base):
    __tablename__ = "children"

    c_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    c_name = Column(String, nullable=False, index=True)
    age_months = Column(Integer, nullable=False, index=True)
    gender = Column(String, nullable=False, index=True)
    weight_kg = Column(Float, nullable=False, index=True)
    height_cm = Column(Float, nullable=False, index=True)
    district_id = Column(Integer, ForeignKey("districts.d_id"), index=True, nullable=True)
    health_worker_id = Column(Integer, ForeignKey("health_worker.h_id"), index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class prediction(base):
    __tablename__ = "prediction"

    p_id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.c_id"), index=True)
    requested_by = Column(Integer, ForeignKey("users.u_id"), nullable=True)
    risk_score = Column(Float, nullable=False)
    risk_catgory = Column(String, nullable=False, index=True)
    confidence = Column(String, nullable=False, index=True)
    reasons = Column(String, nullable=False, index=True)
    model_name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())