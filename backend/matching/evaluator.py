import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def evaluate_requirement(
    requirement: str,
    retrieved_evidence: list[dict]
):
    """
    Use Gemini to decide whether retrieved resume evidence
    actually satisfies a job requirement.

    The LLM can only use the supplied evidence.
    """

    # 1. Nothing was retrieved → no LLM call
    if not retrieved_evidence:
        return {
            "requirement": requirement,
            "matched": False,
            "confidence": 1.0,
            "reason": "No relevant resume evidence found.",
            "evidence": None
        }

    # 2. Prepare evidence for the LLM
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

    # 3. Ask Gemini to evaluate
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # 4. Convert Gemini's JSON response into Python
    result = json.loads(response.text)

    # 5. Add the requirement back to our result
    return {
        "requirement": requirement,
        "matched": result["matched"],
        "confidence": result["confidence"],
        "reason": result["reason"],
        "evidence": result["evidence"]
    }