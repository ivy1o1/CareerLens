import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np
from embeddings import get_embedding, cosine_similarity

MODEL_PATH = "models/all-MiniLM-L6-v2/onnx/model_quint8_avx2.onnx"

tokenizer = AutoTokenizer.from_pretrained("models/all-MiniLM-L6-v2")

session = ort.InferenceSession(MODEL_PATH)

embedding_a = get_embedding("Python backend development")
embedding_b = get_embedding("Building APIs with Python")
embedding_c = get_embedding("Photography and photo editing")

print("A-B:", cosine_similarity(embedding_a, embedding_b))
print("A-C:", cosine_similarity(embedding_a, embedding_c))
