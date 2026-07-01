import os
from datetime import date, datetime

import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

load_dotenv()

app = FastAPI()

hf_token = os.getenv("HF_TOKEN")
model = SentenceTransformer("all-MiniLM-L6-v2", token=hf_token)


def predict_relevance(current_description: str, prior_description: str, threshold: float = 0.90) -> bool:
    embeddings = model.encode(
        [current_description, prior_description],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    similarity = float(np.dot(embeddings[0], embeddings[1]))
    return similarity >= threshold

# 1. Define the lowest level models first
class Study(BaseModel):
    study_id: str
    study_description: str
    study_date: date  # Pydantic will auto-parse "2026-03-08" into a Python date object

# 2. Define the individual case model
class Case(BaseModel):
    case_id: str
    patient_id: str
    patient_name: str
    current_study: Study
    prior_studies: list[Study]  # Handles 0, 1, or many prior studies seamlessly

# 3. Define the root payload wrapper
class ChallengePayload(BaseModel):
    challenge_id: str
    schema_version: int
    generated_at: datetime  # Auto-parses ISO timestamps like "2026-04-16T12:00:00.000Z"
    cases: list[Case]       # Handles any number of cases in the array


# 4. Use it in your route
@app.post("/challenges", status_code=201)
async def process_challenge(payload: ChallengePayload):
    predictions = []

    for case in payload.cases:
        current_description = case.current_study.study_description
        for prior_study in case.prior_studies:
            predictions.append({
                "case_id": case.case_id,
                "study_id": prior_study.study_id,
                "predicted_is_relevant": predict_relevance(
                    current_description,
                    prior_study.study_description,
                ),
            })

    return {"predictions": predictions}
