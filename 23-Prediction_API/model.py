from sqlalchemy import Column, Integer, Float, String, DateTime
from database import base
from sqlalchemy import func


class User(base):
    __tablename__ = "users"

    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    u_role = Column(String, nullable=False, default="Worker")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Child(base):
    __tablename__ = "children"

    c_id = Column(Integer, primary_key=True, index=True)


class prediction_record(base):
    __tablename__ = "predictions"

    p_id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, nullable=False, index=True)
    risk_score = Column(Integer, nullable=False)
    risk_category = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    model_name = Column(String, nullable=False)
    advice = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())