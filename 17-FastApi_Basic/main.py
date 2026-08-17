from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"project": "NourishPak",
            "status": "API running successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy",
            "service": "NourishPak Prediction API"}

@app.get("/project_info")
def project_info():
    return {"project": "NourishPak",
            "description": "Child Malnutrition Risk Prediction System",
            "api_version": 1.0,
            "ml_enabled": True}

@app.get("/model-info")
def model_info():
    return {"model": "Random Forest",
            "task": "Child Malnutrition Risk Classification",
            "status": "trained",
            "classes": ["Low Risk", "High Risk"]}



