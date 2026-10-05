from embeddings import get_embedding, cosine_similarity
from matching.normalizer import normalize_skill


def find_semantic_match(
    job_skill: str,
    resume_skills: list[str],
    threshold: float = 0.6
):
    job_embedding = get_embedding(job_skill)

    best_skill = None
    best_similarity = -1.0

    for resume_skill in resume_skills:
        resume_embedding = get_embedding(resume_skill)

        similarity = cosine_similarity(
            job_embedding,
            resume_embedding
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_skill = resume_skill

    if best_similarity >= threshold:
        return {
            "matched": True,
            "match_type": "semantic",
            "matched_skill": best_skill,
            "similarity": round(float(best_similarity), 4)
        }

    return {
        "matched": False,
        "match_type": "none",
        "matched_skill": None,
        "similarity": round(float(best_similarity), 4)
    }


def match_skills(
    resume_skills: list[str],
    job_skills: list[str],
    threshold: float = 0.6
):
    normalized_resume = {
        normalize_skill(skill): skill
        for skill in resume_skills
    }

    results = []

    for job_skill in job_skills:
        normalized_job_skill = normalize_skill(job_skill)

        # 1. Exact matching first
        if normalized_job_skill in normalized_resume:
            results.append({
                "requirement": job_skill,
                "matched": True,
                "match_type": "exact",
                "matched_skill": normalized_resume[normalized_job_skill],
                "similarity": 1.0
            })

            continue

        # 2. Semantic fallback
        semantic_result = find_semantic_match(
            job_skill,
            resume_skills,
            threshold
        )

        results.append({
            "requirement": job_skill,
            **semantic_result
        })

    return results

def match_requirement(
    requirement: str,
    evidence: list[dict],
    threshold: float = 0.6
):
    # 1. Exact matching first
    normalized_requirement = normalize_skill(requirement)

    for item in evidence:
        if normalize_skill(item["text"]) == normalized_requirement:
            return {
                "requirement": requirement,
                "matched": True,
                "match_type": "exact",
                "similarity": 1.0,
                "evidence": item
            }

    # 2. Semantic matching
    requirement_embedding = get_embedding(requirement)

    best_evidence = None
    best_similarity = -1.0

    for item in evidence:
        evidence_text = item["text"].strip()

        if not evidence_text:
            continue

        evidence_embedding = get_embedding(evidence_text)

        similarity = cosine_similarity(
            requirement_embedding,
            evidence_embedding
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_evidence = item

    similarity = round(float(best_similarity), 4)

    if best_similarity >= threshold:
        return {
            "requirement": requirement,
            "matched": True,
            "match_type": "semantic",
            "similarity": similarity,
            "evidence": best_evidence
        }

    return {
        "requirement": requirement,
        "matched": False,
        "match_type": "none",
        "similarity": similarity,
        "evidence": best_evidence
    }