from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import get_db, authentication
from schemas import (
    userlogin,
    TokenResponse,
    ChildPredictionRequest,
    PredictionResponse,
    PredictionHistoryResponse,
)
from prediction_service import PredictionService
from model import User, Child, prediction_record

app = FastAPI(title="Child Malnutrition API")


@app.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user_data = userlogin(email=form_data.username, password=form_data.password)
    user = authentication.authenticate_user(user_data=user_data, db=db)

    access_token = authentication.create_access_token(
        user_id=user.u_id, email=user.email, role=user.u_role
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        u_id=user.u_id,
        u_name=user.u_name,
        email=user.email,
        u_role=user.u_role,
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def predict_child_health(
    request: ChildPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(authentication.verify_token),
):
    if current_user.u_role not in {"Admin", "Health Worker", "Worker"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )

    child = db.query(Child).filter(Child.c_id == request.child_id).first()
    if not child:
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
            category=saved_record.risk_category,
            confidence=saved_record.confidence,
            advice=saved_record.advice,
            created_at=saved_record.created_at,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during prediction processing: {str(e)}",
        )


@app.get(
    "/children/{child_id}/predictions",
    response_model=PredictionHistoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_child_predictions(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(authentication.verify_token),
):
    child = db.query(Child).filter(Child.c_id == child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child not found"
        )

    records = (
        db.query(prediction_record)
        .filter(prediction_record.child_id == child_id)
        .order_by(prediction_record.created_at.desc())
        .all()
    )

    formatted_predictions = [
        {
            "risk_score": r.risk_score,
            "category": r.risk_category,
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