from typing import List
import pandas as pd
import numpy as np
from fastapi import FastAPI
import xgboost
from xgboost import XGBClassifier

from data_model import DataModel
from data_model_retrain import DataModelRetrain
from prediction_model import PredictionModel
from retrain_model import RetrainModel



app = FastAPI()


@app.get("/")
def read_root():
   return { "message": "Hello world" }

@app.post("/predict")
def make_predictions(X: List[DataModel]):
    df = pd.DataFrame([x.dict() for x in X])
    predicion_model = PredictionModel()
    results = predicion_model.make_predictions(df)
    return results.tolist()

# Added to retrain the model
@app.post("/retrain")
def retrain(X: List[DataModelRetrain]):
    df = pd.DataFrame([x.dict() for x in X])
    retrain_model = RetrainModel()
    metrics_original, metrics_retrain = retrain_model.make_retrain(df)
    results = {"Original": metrics_original, "Re-entrenado" : metrics_retrain}
    retrain_model.save_model()
    return results