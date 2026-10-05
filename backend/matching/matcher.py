from embeddings import get_embedding, cosine_similarity
from matching.normalizer import normalize_skill


def retrieve_evidence(
    requirement: str,
    evidence: list[dict],
    top_k: int = 3
):
    """
    Retrieve the most relevant resume evidence for a job requirement.

    This function does NOT decide whether the candidate qualifies.
    It only finds potentially relevant evidence.
    """

    if not evidence:
        return []

    normalized_requirement = normalize_skill(requirement)

    # Exact matches should always rank first.
    scored_evidence = []

    requirement_embedding = get_embedding(requirement)

    for item in evidence:
        text = item.get("text", "").strip()

        if not text:
            continue

        normalized_text = normalize_skill(text)

        if normalized_text == normalized_requirement:
            similarity = 1.0
            match_type = "exact"
        else:
            evidence_embedding = get_embedding(text)

            similarity = cosine_similarity(
                requirement_embedding,
                evidence_embedding
            )

            match_type = "semantic"

        scored_evidence.append({
            "evidence": item,
            "similarity": round(float(similarity), 4),
            "match_type": match_type
        })

    # Highest similarity first
    scored_evidence.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return scored_evidence[:top_k]