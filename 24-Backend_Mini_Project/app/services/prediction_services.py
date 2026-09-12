import os
import joblib
import pandas as pd
from fastapi import HTTPException, status
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models import prediction, child


class PredictionService:
    model = None

    @classmethod
    def load_model(cls, path:str="app/ml_models/Random Forest Model.pkl") -> None:
        model_path = path
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")

        try:
            cls.model = joblib.load(model_path)
            print("ML Model Loaded Successfully")
        except Exception:
            import pickle

            with open(model_path, "rb") as f:
                cls.model = pickle.load(f)
            print("ML Model Loaded Successfully")

    @classmethod
    def prepare_input(cls, payload: Dict[str, Any]) -> pd.DataFrame:
        df = pd.DataFrame([payload])

        column_mapping = {
            "age_months": "Age (months)",
            "gender": "Gender",
            "household_wealth_index": "Household_Wealth_Index",
            "height_cm": "Height_cm",
            "mother_education": "Mother_Education",
            "weight_kg": "Weight_kg",
        }

        df = df.rename(columns=column_mapping)

        feature_columns = [
            "Age (months)",
            "Gender",
            "Household_Wealth_Index",
            "Height_cm",
            "Mother_Education",
            "Weight_kg",
        ]
        for col in feature_columns:
            if col not in df.columns:
                df[col] = None

        return df[feature_columns]

    @classmethod
    def calculate_risk_score(cls, df_prepared: pd.DataFrame) -> tuple[int, float]:
        if hasattr(cls.model, "predict_proba"):
            probabilities = cls.model.predict_proba(df_prepared)[0]
            high_risk_prob = float(probabilities[-1])
            risk_score = int(round(high_risk_prob * 100))
            confidence = round(high_risk_prob * 100, 2)
        else:
            raw_pred = cls.model.predict(df_prepared)[0]
            risk_score = 100 if str(raw_pred).lower() in ["high risk", "1"] else 0
            confidence = 100.0
        return risk_score, confidence

    @classmethod
    def determine_risk_category(cls, risk_score: int) -> str:
        if risk_score >= 70:
            return "High Risk"
        elif risk_score >= 35:
            return "Medium Risk"
        return "Low Risk"

    @classmethod
    def generate_advice(cls, category: str) -> str:
        if category == "Low Risk":
            return "Continue regular growth monitoring and healthy nutrition practices."
        elif category == "Medium Risk":
            return "Schedule follow-up assessment and review feeding practices."
        else:
            return "Refer child for nutrition support and further clinical assessment."

    @classmethod
    def save_prediction(
        cls,
        db: Session,
        child_id: int,
        risk_score: int,
        risk_category: str,
        confidence: float,
        advice: str,
        model_name: str = "Random_Forest_Classifier",
    ) -> prediction:
        record = prediction(
            child_id=child_id,
            risk_score=risk_score,
            risk_category=risk_category,
            confidence=confidence,
            model_name=model_name,
            advice=advice,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def predict_health_by_child_id(cls, db: Session, child_id: int):
        db_child = db.query(child).filter(child.c_id == child_id).first()
        if not db_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found in the database"
            )

        if cls.model is None:
            cls.load_model()

        payload = {
            "age_months": db_child.age_months,
            "gender": db_child.gender,
            "mother_education": db_child.mother_education,
            "household_wealth_index": db_child.household_wealth_index,
            "weight_kg": db_child.weight_kg,
            "height_cm": db_child.height_cm,
        }

        input_feature = cls.prepare_input(payload)
        risk_score, confidence = cls.calculate_risk_score(input_feature)
        risk_category = cls.determine_risk_category(risk_score)
        advice = cls.generate_advice(risk_category)

        return cls.save_prediction(
            db=db,
            child_id=child_id,
            risk_score=risk_score,
            risk_category=risk_category,
            confidence=confidence,
            advice=advice
        )

    @classmethod
    def get_latest_prediction(cls, db: Session):
        latest_record = (
            db.query(prediction)
            .order_by(prediction.created_at.desc())
            .first()
        )
        if not latest_record:
            return {
                "message": "No prediction found for this child"
            }
        return latest_record


PredictionService.load_model()