import joblib
import os
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "model", "rf_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_hit(features: list):
    X = np.array(features).reshape(1, -1)
    proba_is_hit = model.predict_proba(X)[0][1]
    pred = "Hit" if proba_is_hit >= 0.5 else "Not Hit"
    return {"hit_probability": round(proba_is_hit, 3), "prediction": pred}