from embeddings import get_embedding, cosine_similarity
from matching.normalizer import normalize_skill
from matching.evaluator import evaluate_requirement

def retrieve_evidence(
    requirement: str,
    evidence: list[dict],
    top_k: int = 3,
    min_similarity: float = 0.4
):
    """
    Retrieve the strongest relevant resume evidence.

    The retriever finds potentially useful evidence.
    It does NOT decide whether the candidate qualifies.
    """

    if not evidence:
        return []

    normalized_requirement = normalize_skill(requirement)
    requirement_embedding = get_embedding(requirement)

    scored_evidence = {}

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

        similarity = float(similarity)

        # Ignore obviously weak candidates
        if similarity < min_similarity:
            continue

        # Keep only the strongest occurrence of duplicate evidence
        existing = scored_evidence.get(normalized_text)

        result = {
            "evidence": item,
            "similarity": round(similarity, 4),
            "match_type": match_type
        }

        if existing is None or similarity > existing["similarity"]:
            scored_evidence[normalized_text] = result

    results = list(scored_evidence.values())

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]


def match_requirements(
    requirements: list[str],
    evidence: list[dict]
):
    """
    Match every job requirement against resume evidence.

    Retrieval happens first.
    Gemini evaluation happens second.
    """

    results = []

    for requirement in requirements:

        retrieved_evidence = retrieve_evidence(
            requirement,
            evidence
        )

        evaluation = evaluate_requirement(
            requirement,
            retrieved_evidence
        )

        results.append(evaluation)

    return results