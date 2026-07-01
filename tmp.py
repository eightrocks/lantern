import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
model = SentenceTransformer("BAAI/bge-base-en-v1.5", token=hf_token)


def predict_relevance(current_description: str, prior_description: str, threshold: float = 0.90) -> bool:
    embeddings = model.encode([current_description, prior_description], convert_to_numpy=True)
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(similarity) >= threshold


current_description = "MRI BRAIN STROKE LIMITED WITHOUT CONTRAST"
prior_descriptions = [
    "MRI BRAIN STROKE LIMITED WITHOUT CONTRAST",
    "CT HEAD WITHOUT CNTRST",
]

for prior_description in prior_descriptions:
    embeddings = model.encode([current_description, prior_description], convert_to_numpy=True)
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    is_relevant = predict_relevance(current_description, prior_description)
    print(f"{prior_description}: similarity={score:.3f}, predicted_is_relevant={is_relevant}")