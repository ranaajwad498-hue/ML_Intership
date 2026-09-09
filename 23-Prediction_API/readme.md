# ML Risk Prediction API

A FastAPI service that wraps a trained machine learning model to generate **health risk scores**, persist predictions to PostgreSQL, and expose a history endpoint — all protected by JWT authentication. This service evolves the standalone **Day 15 Python prediction engine** into a production-ready, database-backed, auth-protected REST API.

> **Note:** Where project-specific values (model type, exact feature set, thresholds) aren't fixed in your codebase yet, this README documents the standard/reference implementation used across this service — adjust to match your actual `model.pkl` and schema if they differ.

---

## Table of Contents

1. [ML Model Used](#ml-model-used)
2. [Input Features](#input-features)
3. [Prediction Endpoint](#prediction-endpoint)
4. [Preprocessing Flow](#preprocessing-flow)
5. [Risk Score Calculation](#risk-score-calculation)
6. [Risk Categories](#risk-categories)
7. [Advice Generation](#advice-generation)
8. [JWT Protection](#jwt-protection)
9. [PostgreSQL Prediction Storage](#postgresql-prediction-storage)
10. [Prediction History](#prediction-history)
11. [Sample Request and Response](#sample-request-and-response)
12. [Comparison with the Day 15 Python Prediction Engine](#comparison-with-the-day-15-python-prediction-engine)
13. [How This API Can Later Be Consumed by the Flutter Mobile Application](#how-this-api-can-later-be-consumed-by-the-flutter-mobile-application)

---

## ML Model Used

The service uses a **scikit-learn `RandomForestClassifier`** (binary classification: high-risk vs. low-risk), trained offline and serialized with `joblib`. Random Forest was chosen over a single decision tree or logistic regression because it:

- Handles non-linear relationships between features without manual feature engineering.
- Is robust to outliers and doesn't require strict feature scaling (though scaling is still applied for consistency with other models tested).
- Provides `predict_proba()`, giving a continuous probability we convert into a risk score, rather than only a hard class label.

The model artifact is loaded once at application startup (not per-request) to avoid repeated disk I/O:

```python
import joblib
from pathlib import Path

MODEL_PATH = Path("ml_models/Random_Forest_Classifier.joblib")

model = joblib.load(MODEL_PATH)

```

```python
@app.on_event("startup")
async def load_ml_artifacts():
    app.state.model = joblib.load(MODEL_PATH)
```

---

## Input Features

| Feature | Type | 
|---|---|
| `age (months)` | int |
| `gender` | string |  
| `houshold_wealth` | string | 
| `mother_education` | string | 
| `weight_kg` | float | 
| `height_cm` | float | 

Pydantic schema enforces types and ranges at the request boundary:

```python
from pydantic import BaseModel, Field
class ChildPredictionRequest(BaseModel):
    child_id: int = Field(..., gt=0, example=101)
    age_months: float = Field(..., ge=0, example=18.0)
    gender: Literal["Male", "Female"]
    mother_education: Literal["No education", "Primary", "Secondary", "Higher"] = Field(
        "Secondary", example="Secondary"
    )
    household_wealth_index: Literal["Poorest", "Poor", "Middle", "Richer", "Richest"] = Field(
        "Middle", example="Middle"
    )
    weight_kg: float = Field(..., gt=0, example=7.8)
    height_cm: float = Field(..., gt=0, example=74.0)
```

---

## Prediction Endpoint

```
POST /predict
```

- **Auth**: Required (JWT bearer token)
- **Content-Type**: `application/json`
- **Body**: `RiskPredictionInput`

```python
@router.post("/predict", response_model=PredictionResponse)
async def predict_risk(
    payload: RiskPredictionInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    features = preprocess(payload)
    probability = model.predict_proba(features)[0][1]
    score = calculate_risk_score(probability)
    category = categorize_risk(score)
    advice = generate_advice(category, payload)

    record = prediction_record(
        user_id=current_user.id,
        input_data=payload.dict(),
        risk_score=score,
        risk_category=category,
        advice=advice,
    )
    db.add(record)
    db.commit()
    db.refresh(prediction)

    return prediction
```

---

## Preprocessing Flow

Raw JSON input is transformed into the exact numerical format the model expects, in this order:

1. **Schema validation** — Pydantic rejects malformed or out-of-range values before preprocessing starts.
2. **Ordering** — features are arranged into a fixed column order matching the training pipeline (order matters for the model, not field names).
3. **Encoding** — categorical fields (`houshold_wealth`, `mother_education`) are already integer-encoded at input time, matching the encoding used during training.
4. **Scaling** — continuous features (`age`, `height_cm`, `weight_kg`) are transformed with the same `StandardScaler` fitted during training.
5. **Reshape** — flattened into a single-row 2D array (`1 x n_features`) since scikit-learn expects a 2D input even for one sample.



---

## Risk Score Calculation

The model's `predict_proba()` returns the probability of the positive (high-risk) class, a float between 0 and 1. This is converted into a **0–100 risk score** for easier interpretation by end users:

```python
def calculate_risk_score(probability: float) -> float:
    """Convert model probability (0-1) into a 0-100 risk score."""
    return round(probability * 100, 2)
```

We use the probability rather than the raw class label (`0`/`1`) because a binary label loses information — a 51% and a 98% prediction are both "high risk" as a label, but represent very different levels of concern for the user and for the advice engine.

---

## Risk Categories

The numeric score is bucketed into three human-readable categories:

| Score Range | Category |
|---|---|
| 0 – 33 | `Low` |
| 34 – 66 | `Moderate` |
| 67 – 100 | `High` |

```python
def categorize_risk(score: float) -> str:
    if score <= 33:
        return "Low"
    elif score <= 66:
        return "Moderate"
    return "High"
```

Thresholds are defined as constants (not magic numbers inline) so they can be tuned as the model is retrained without touching endpoint logic:

```python
RISK_THRESHOLDS = {"low_max": 33, "moderate_max": 66}
```

---

## Advice Generation

Advice is **rule-based**, not model-generated — the ML model only produces a score; a separate deterministic layer maps `(category, input features)` to actionable guidance. This keeps advice auditable and easy to update without retraining the model.

```python
    def generate_advice(cls, category: str) -> str:
        if category == "Low Risk":
            return "Continue regular growth monitoring and healthy nutrition practices."
        elif category == "Medium Risk":
            return "Schedule follow-up assessment and review feeding practices."
        else:
            return "Refer child for nutrition support and further clinical assessment."
```

This produces a small, ordered list of relevant tips rather than a generic paragraph, and each rule is independently testable.

---

## JWT Protection

Every endpoint in this service — prediction and history alike — depends on `get_current_user`, which validates the bearer token before any model or database logic executes.

```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

Requests without a valid token receive `401 Unauthorized`. Predictions are always tied to `current_user.id`, so one user can never see or trigger predictions for another.

---

## PostgreSQL Prediction Storage

### `predictions` table

| Column | Type | Notes |
|---|---|---|
| `id` | `UUID PRIMARY KEY` | |
| `user_id` | `INTEGER REFERENCES users(id)` | owner, indexed |
| `input_data` | `JSONB` | raw request payload, for auditability/reproducibility |
| `risk_score` | `NUMERIC(5,2)` | 0–100 |
| `risk_category` | `VARCHAR(20)` | `Low` / `Moderate` / `High` |
| `advice` | `JSONB` | list of generated advice strings |
| `model_version` | `VARCHAR(50)` | tag of the model artifact used |
| `created_at` | `TIMESTAMP DEFAULT now()` | |

```sql
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    input_data JSONB NOT NULL,
    risk_score NUMERIC(5,2) NOT NULL,
    risk_category VARCHAR(20) NOT NULL,
    advice JSONB NOT NULL,
    model_version VARCHAR(50) NOT NULL DEFAULT 'v1',
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
```

SQLAlchemy model:

```python
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    input_data = Column(JSONB, nullable=False)
    risk_score = Column(Numeric(5, 2), nullable=False)
    risk_category = Column(String(20), nullable=False)
    advice = Column(JSONB, nullable=False)
    model_version = Column(String(50), nullable=False, default="v1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

Storing `input_data` and `model_version` alongside the result means any past prediction can be explained or reproduced later, even after the model is retrained.

---

## Prediction History

```
GET /api/v1/predict/history
```

- **Auth**: Required
- Returns the authenticated user's past predictions, most recent first.
- Supports pagination via `limit` / `offset` query parameters.

```python
@router.get("/predict/history", response_model=list[PredictionResponse])
async def get_prediction_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    history = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return history
```

---

## Sample Request and Response

### Predict Risk

**Request**

```bash
curl -X POST "https://api.example.com/api/v1/predict" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
  "child_id": 1,
  "age_months": 18,
  "gender": "Male",
  "mother_education": "Secondary",
  "household_wealth_index": "Middle",
  "weight_kg": 7.8,
  "height_cm": 74
}'
```

**Response `200 OK`**

```json
{
  "p_id": 3,
  "child_id": 1,
  "risk_score": 47,
  "category": "Medium Risk",
  "confidence": 46.54,
  "advice": "Schedule follow-up assessment and review feeding practices.",
  "created_at": "2026-09-02T16:21:38.951290+05:00"
  ],
  "model_version": "v1",
  "created_at": "2026-09-01T09:20:00Z"
}
```

### Prediction History

**Request**

```bash
curl -X GET "https://api.example.com/api/v1/predict/history?limit=5" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Response `200 OK`**

```json
[
  "child_id": 1,
  "total_predictions": 3,
  "predictions": [
    {
      "risk_score": 47,
      "category": "Medium Risk",
      "confidence": 46.54,
      "created_at": "2026-09-02T16:21:38.951290+05:00"
    }
]
```

### Error Example — Invalid Input

```json
{
  "detail": [
    {
      "loc": ["body","age_months"],
      "msg": "ensure this value is greator than or equal to 1",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

## Comparison with the Day 15 Python Prediction Engine

| Aspect | Day 15 Engine | This API |
|---|---|---|
| **Interface** | Local Python script (CLI or notebook), run manually | HTTP REST endpoint (`POST /api/v1/predict`), callable remotely |
| **Input handling** | Hardcoded or manually entered variables | Validated JSON body via Pydantic, with type/range enforcement |
| **Preprocessing** | Inline, ad-hoc scaling/encoding in the script | Extracted into a reusable `preprocess()` function, matching a versioned scaler artifact |
| **Output** | Printed probability/class to console | Structured JSON response with score, category, advice, and metadata |
| **Persistence** | None — results existed only in the terminal/notebook session | Every prediction is persisted to PostgreSQL with full input/output for audit and history |
| **Authentication** | None — anyone running the script had full access | JWT-protected; predictions are scoped to the authenticated user |
| **Advice** | Not present, or manually reasoned about by the developer | Automated rule-based advice generation layered on top of the score |
| **Reusability** | Single-user, single-run | Multi-user, multi-client (web, mobile, other services) via a stable API contract |
| **Model versioning** | Implicit — whatever `model.pkl` was loaded that session | Explicit `model_version` field stored per prediction |

In short, the Day 15 engine proved the model works; this API turns that engine into a **service** — network-accessible, authenticated, auditable, and stateful — which is what a real application (including a mobile client) needs to consume.

---

## How This API Can Later Be Consumed by the Flutter Mobile Application

Because the service is a standard JSON-over-HTTPS REST API with JWT auth, it can be consumed by a Flutter app the same way any other backend would be, with no ML-specific tooling needed on the mobile side:

1. **Authentication** — the Flutter app calls the existing `/login` endpoint, stores the returned JWT securely (e.g., via `flutter_secure_storage`), and attaches it as an `Authorization: Bearer <token>` header on subsequent requests.

2. **HTTP client** — using a package like `dio` or `http`, the app builds a request body matching `RiskPredictionInput` from form fields (age, BMI, blood pressure, etc.) collected in a Flutter form/wizard UI.

   ```dart
   final response = await dio.post(
     'https://api.example.com/api/v1/predict',
     data: {
      "child_id": 1,
      "age_months": 18,
      "gender": "Male",
      "mother_education": "Secondary",
      "household_wealth_index": "Middle",
      "weight_kg": 7.8,
      "height_cm": 74
     },
     options: Options(headers: {"Authorization": "Bearer $jwtToken"}),
   );
   ```

3. **Rendering the result** — the JSON response (`risk_score`, `risk_category`, `advice`) maps directly onto a result screen: a gauge/progress widget for the score, a colored badge for the category (green/yellow/red), and a bulleted list for advice.

4. **History screen** — the app calls `GET /api/v1/predict/history` to populate a list/timeline view of past assessments, enabling trend charts (e.g., score over time) using a charting package like `fl_chart`.

5. **Offline/error handling** — since the mobile network is less reliable than a browser session, the app should handle `401` by refreshing the token or redirecting to login, and handle `4xx` validation errors by surfacing field-level messages back onto the form.

6. **No model logic on-device** — because inference happens entirely server-side, the Flutter app never needs to bundle the model, scaler, or any ML runtime, keeping the app lightweight and ensuring every user always hits the latest deployed model version.

This separation — Flutter as a thin presentation layer, FastAPI as the stateful, authenticated ML service — is exactly why building this as a REST API (rather than embedding the Day 15 script's logic into the app) pays off: the same backend can later serve a web dashboard, admin panel, or third-party integration without any duplicated prediction logic.
