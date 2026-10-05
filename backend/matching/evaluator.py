import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)


def evaluate_requirement(
    requirement: str,
    retrieved_evidence: list[dict]
):
    """
    Use Gemini to decide whether retrieved resume evidence
    actually satisfies a job requirement.
    """

    # No evidence → no need to call Gemini
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
You are evaluating whether a candidate's resume evidence
satisfies a job requirement.

JOB REQUIREMENT:
{requirement}

RESUME EVIDENCE:
{json.dumps(evidence_text, indent=2)}

RULES:
1. Use ONLY the supplied resume evidence.
2. Do not invent experience, skills, or qualifications.
3. Semantic similarity alone does NOT prove qualification.
4. The evidence must actually support the requirement.
5. If the evidence is insufficient or only loosely related, return matched=false.
6. Keep the reason short and factual.

Return ONLY valid JSON in this exact format:

{{
    "matched": true,
    "confidence": 0.95,
    "reason": "The candidate explicitly demonstrates the required skill.",
    "evidence": "The strongest supporting evidence."
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Gemini may wrap JSON inside ```json ... ```
    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "", 1)
        response_text = response_text.replace("```", "", 1)
        response_text = response_text.strip()

    result = json.loads(response_text)

    return {
        "requirement": requirement,
        "matched": result["matched"],
        "confidence": result["confidence"],
        "reason": result["reason"],
        "evidence": result["evidence"]
    }