from fastapi import FastAPI
from app.routers import auth, children,prediction  

app = FastAPI(title="Backend Mini Project")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(children.router, prefix="/children", tags=["Children"])
app.include_router(prediction.router, prefix="/prediction", tags=["Prediction"])
