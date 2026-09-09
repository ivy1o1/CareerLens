import os

from dotenv import load_dotenv
from google import genai

from models import Resume


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def extract_resume_data(text: str):
    prompt = f"""
    Extract information from this resume and return it according to the provided schema.

    Follow these rules carefully:

    1. EXPERIENCE:
        Include jobs, internships, and organizational roles where the person
        performed responsibilities or contributed to an organization.
        Do NOT copy experience into achievements.

    2. PROJECTS:
        Include things the person built, developed, researched, or worked on
        as a distinct project.
        Do NOT treat jobs or organizational roles as projects.

    3. CERTIFICATIONS:
        Include only formal certifications, certificates, or credentials.
        Do NOT infer certifications from skills or courses.

    4. ACHIEVEMENTS:
        Include awards, competition results, rankings, prizes, honors,
        or other explicitly stated accomplishments.
        Do NOT include jobs, roles, responsibilities, or society memberships
        unless they are explicitly described as an achievement.

    5. SKILLS:
        - technical: programming languages, frameworks, technical concepts
        - tools: software, platforms, and AI tools
        - soft: communication, leadership, teamwork, organization, etc.

    6. MISSING INFORMATION:
        If something is not explicitly present, use null for optional fields
        or an empty list for list fields.
        Never guess, infer, or invent information.

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