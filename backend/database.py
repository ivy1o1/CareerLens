import os
from dotenv import load_dotenv
from supabase import create_client

from models import Resume

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase = create_client(supabase_url, supabase_key)

def save_resume(resume: Resume):
    data = {
        "name": resume.personal_info.name,
        "email": resume.personal_info.email,
        "phone": resume.personal_info.phone,
        "education": [item.model_dump() for item in resume.education],
        "skills": resume.skills.model_dump(),
        "experience": [item.model_dump() for item in resume.experience],
        "projects": [item.model_dump() for item in resume.projects],
        "certifications": [item.model_dump() for item in resume.certifications],
        "achievements": [item.model_dump() for item in resume.achievements],
    }

    response = supabase.table("resumes").insert(data).execute()

    return response.data

def save_job(job: dict):
    data = {
        "title": job["title"],
        "company": job["company"],
        "description": job.get("description"),
        "required_skills": job.get("required_skills", []),
        "location": job.get("location"),
        "job_type": job.get("job_type"),
        "application_url": job.get("application_url"),
    }

    response = supabase.table("jobs").insert(data).execute()

    return response.data