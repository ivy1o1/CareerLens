import os
import json

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from matching.matcher import retrieve_evidence


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)


class EvaluationResult(BaseModel):
    matched: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    evidence: str | None


def evaluate_requirement(
    requirement: str,
    retrieved_evidence: list[dict]
):
    """
    Decide whether retrieved resume evidence
    actually satisfies a job requirement.
    """

    # No evidence → don't call Gemini
    if not retrieved_evidence:
        return {
            "requirement": requirement,
            "matched": False,
            "confidence": 1.0,
            "reason": "No relevant resume evidence found.",
            "evidence": None
        }

    evidence_text = []

    for item in retrieved_evidence:
        evidence = item["evidence"]

        evidence_text.append({
            "text": evidence["text"],
            "source_type": evidence["source_type"],
            "source_name": evidence.get("source_name"),
            "similarity": item["similarity"]
        })

    prompt = f"""
Evaluate whether the supplied resume evidence satisfies the job requirement.

JOB REQUIREMENT:
{requirement}

RESUME EVIDENCE:
{json.dumps(evidence_text, indent=2)}

RULES:
1. Use ONLY the supplied resume evidence.
2. Do not invent skills, experience, or qualifications.
3. Semantic similarity does not prove qualification.
4. The evidence must directly support the requirement.
5. If the evidence is insufficient or only loosely related, matched must be false.
6. Keep the reason short and factual.
7. evidence must contain the strongest supporting resume evidence,
   or null if there is no supporting evidence.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": EvaluationResult,
        },
    )

    result = EvaluationResult.model_validate_json(response.text)

    return {
        "requirement": requirement,
        **result.model_dump()
    }
    
def evaluate_requirements(
    requirements: list[str],
    evidence: list[dict]
):
    """
    Evaluate every job requirement against resume evidence.
    """

    results = []

    for requirement in requirements:
        retrieved_evidence = retrieve_evidence(
            requirement,
            evidence
        )

        result = evaluate_requirement(
            requirement,
            retrieved_evidence
        )

        results.append(result)

    return results