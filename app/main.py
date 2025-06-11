from fastapi import FastAPI
from pydantic import BaseModel
from app.model_utils import predict_hit

app = FastAPI()

class SongFeatures(BaseModel):
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float

@app.post("/predict")
def predict_song(features: SongFeatures):
    feature_list = list(features.dict().values())
    return predict_hit(feature_list)