from database import base
from sqlalchemy import BigInteger, Column, Integer, String, DateTime
from sqlalchemy.sql import func


class Child(base):
    __tablename__ = "children"

    c_id = Column(Integer, primary_key=True, index=True)
    c_name = Column(String, nullable=False, index=True)
    age_months = Column(Integer, nullable=False, index=True)
    gender = Column(String, nullable=False, index=True)
    weight_kg = Column(Integer, nullable=False, index=True)
    height_cm = Column(Integer, nullable=False, index=True)
    district_id = Column(BigInteger, nullable=False, index=True)
    health_worker_id = Column(BigInteger, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())