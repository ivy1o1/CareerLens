from embeddings import get_embedding, cosine_similarity


pairs = [
    (
        "Python backend development",
        "Building APIs with Python"
    ),
    (
        "Python backend development",
        "Backend development using Python and FastAPI"
    ),
    (
        "Python backend development",
        "Frontend development with React"
    ),
    (
        "Python backend development",
        "Photography and photo editing"
    ),
    (
        "FastAPI REST API development",
        "Building web APIs with Python"
    ),
    (
        "FastAPI REST API development",
        "Graphic design and Photoshop"
    )
]


for i, (text_a, text_b) in enumerate(pairs, start=1):

    embedding_a = get_embedding(text_a)
    embedding_b = get_embedding(text_b)

    score = cosine_similarity(
        embedding_a,
        embedding_b
    )

    print(f"\nPair {i}")
    print("A:", text_a)
    print("B:", text_b)
    print("Cosine similarity:", round(float(score), 4))