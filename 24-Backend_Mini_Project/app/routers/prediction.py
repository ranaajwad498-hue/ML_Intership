from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import ChildPredictionRequest,PredictionResponse,PredictionHistoryResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authentication
from app.models import users,child,prediction
from app.services.prediction_services import PredictionService

router = APIRouter()

@router.post("/predict",response_model=PredictionResponse,status_code=status.HTTP_201_CREATED,)
def predict_child_health(request: ChildPredictionRequest,db: Session = Depends(get_db),current_user: users = Depends(authentication.verify_token)):
    if current_user.u_role not in {"Admin", "Health Worker", "Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )
    childs = db.query(child).filter(child.c_id == request.child_id).first()
    if not childs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child not found"
        )

    try:
        payload = request.model_dump()
        df_prepared = PredictionService.prepare_input(payload)

        risk_score, confidence = PredictionService.calculate_risk_score(
            df_prepared
        )
        risk_category = PredictionService.determine_risk_category(risk_score)
        advice = PredictionService.generate_advice(risk_category)

        saved_record = PredictionService.save_prediction(
            db=db,
            child_id=request.child_id,
            risk_score=risk_score,
            risk_category=risk_category,
            confidence=confidence,
            advice=advice,
        )

        return PredictionResponse(
            p_id=saved_record.p_id,
            child_id=saved_record.child_id,
            risk_score=saved_record.risk_score,
            risk_category=saved_record.risk_category,
            confidence=saved_record.confidence,
            advice=saved_record.advice,
            created_at=saved_record.created_at,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during prediction processing: {str(e)}",
        )


@router.post("/children/{child_id}/predict", response_model=PredictionResponse)
def predict_child_health_by_id(child_id: int,db: Session = Depends(get_db),current_user: users = Depends(authentication.verify_token),):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )
    record = PredictionService.predict_health_by_child_id(db=db, child_id=child_id)
    return PredictionResponse(
    p_id=record.p_id,
    child_id=record.child_id,
    risk_score=record.risk_score,
    risk_category=record.risk_category,
    confidence=float(record.confidence),
    advice=record.advice,
    created_at=record.created_at
)


@router.get("/children/{child_id}/predictions",response_model=PredictionHistoryResponse,status_code=status.HTTP_200_OK,)
def get_child_predictions_history(child_id: int,db: Session = Depends(get_db),current_user: users = Depends(authentication.verify_token),):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )
    childs = db.query(child).filter(child.c_id == child_id).first()
    if not childs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child not found"
        )

    records = (
        db.query(prediction)
        .filter(prediction.child_id == child_id)
        .order_by(prediction.created_at.desc())
        .all()
    )

    formatted_predictions = [
        {
            "risk_score": r.risk_score,
            "risk_category": r.risk_category,
            "confidence": r.confidence,
            "created_at": r.created_at,
        }
        for r in records
    ]

    return PredictionHistoryResponse(
        child_id=child_id,
        total_predictions=len(formatted_predictions),
        predictions=formatted_predictions,
    )

@router.get("/prediction/latest", response_model=PredictionResponse)
def get_latest_prediction(db: Session = Depends(get_db),current_user: users = Depends(authentication.verify_token),):
    if current_user.u_role not in {"Admin", "Health_worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )
    record = PredictionService.get_latest_prediction(db=db)
    return PredictionResponse.model_validate(record)