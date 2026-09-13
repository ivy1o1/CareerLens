import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np


MODEL_PATH = "models/all-MiniLM-L6-v2/onnx/model_quint8_avx2.onnx"

tokenizer = AutoTokenizer.from_pretrained("models/all-MiniLM-L6-v2")
session = ort.InferenceSession(MODEL_PATH)


def get_embedding(text):
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

    return embedding[0]

def cosine_similarity(embedding_a, embedding_b):
    return np.dot(embedding_a, embedding_b) / (
        np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b)
    )