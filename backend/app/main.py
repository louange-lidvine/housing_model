from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import HouseData
from .ml_model.train_model import load_model
from fastapi import Request

import pandas as pd
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000/"
]


# Enable CORS
# CORS (Cross-Origin Resource Sharing) middleware configuration

app = FastAPI()

@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)

# Load model and feature columns
model, feature_columns = load_model()

@app.get("/api/test")
async def test():
    return {"message": "API is working through Nginx!"}

@app.post("/predict/")
async def predict_price(house: HouseData):
    input_data = pd.DataFrame([house.dict()])
    input_data = pd.get_dummies(input_data)
    for col in feature_columns:
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[feature_columns]
    predicted_price = model.predict(input_data)[0]
    return {"predicted_price": round(predicted_price, 2)}
