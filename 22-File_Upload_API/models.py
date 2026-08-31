from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Float
from database import base
from sqlalchemy import func

class Children(base):
    __tablename__ = "children"

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


class child_documents(base):
    __tablename__ = "child_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.c_id"))
    original_name = Column(String, nullable=False, index=True)
    stored_name = Column(String, nullable=False, index=True)
    file_path = Column(String, nullable=False, index=True)
    file_type = Column(String, nullable=False, index=True)
    uploaded_by = Column(Integer, ForeignKey("users.u_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(base):
    __tablename__ = "users"

    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    u_role = Column(String, nullable=False, default="Worker")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())