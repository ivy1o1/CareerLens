import os

from dotenv import load_dotenv
from google import genai

from models import Resume


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def extract_resume_data(text: str):
    prompt = f"""
    Extract the information from this resume.

    Organize skills into:
    - technical: programming languages, frameworks, technical concepts
    - tools: software, platforms, and AI tools
    - soft: communication, leadership, teamwork, organization, etc.

    If information is not present, return null for optional fields
    or an empty list for list fields. Do not guess or invent information.

    Resume text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Resume,
        },
    )

    return response.parsed