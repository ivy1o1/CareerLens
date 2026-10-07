import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np


MODEL_PATH = "models/all-MiniLM-L6-v2/onnx/model_quint8_avx2.onnx"

tokenizer = AutoTokenizer.from_pretrained("models/all-MiniLM-L6-v2")
session = ort.InferenceSession(MODEL_PATH)


def get_embedding(text: str) -> np.ndarray:
    inputs = tokenizer(
        text,
        return_tensors="np",
        padding=True,
        truncation=True
    )

    outputs = session.run(None, dict(inputs))

    token_embeddings = outputs[0]
    attention_mask = inputs["attention_mask"]

    mask = attention_mask[..., None]
    masked_embeddings = token_embeddings * mask

    sum_embeddings = masked_embeddings.sum(axis=1)
    sum_mask = mask.sum(axis=1)

    embedding = sum_embeddings / sum_mask
    embedding = embedding[0]

    norm = np.linalg.norm(embedding)

    if norm == 0:
        raise ValueError("Cannot normalize a zero-vector embedding.")

    return embedding / norm


def cosine_similarity(
    embedding_a: np.ndarray,
    embedding_b: np.ndarray
) -> float:
    norm_a = np.linalg.norm(embedding_a)
    norm_b = np.linalg.norm(embedding_b)

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Cosine similarity requires non-zero vectors.")

    return float(np.dot(embedding_a, embedding_b) / (norm_a * norm_b))