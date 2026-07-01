import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

hf_token = os.getenv("HF_TOKEN")

model = SentenceTransformer("all-MiniLM-L6-v2", token=hf_token)

A = "MRI BRAIN STROKE LIMITED WITHOUT CONTRAST"
B = "MRI BRAIN STROKE LIMITED WITHOUT CONTRAST"
C = "CT HEAD WITHOUT CNTRST"

embeddings = model.encode(
    [A, C],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

embeddings2 = model.encode(
    [B, A],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

score1 = float(np.dot(embeddings[0], embeddings[1]))
score2 = float(np.dot(embeddings2[0], embeddings2[1]))

print(score1)
print(score2)