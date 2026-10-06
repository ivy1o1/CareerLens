import pymupdf
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv

from database import save_job, supabase, save_resume
from fastapi import HTTPException
from models import(
    Resume,
    Job
)
from resume_parser import extract_resume_data
from matching.evidence import build_resume_evidence
from matching.matcher import match_requirements


app = FastAPI()

@app.get("/")
def home():
    return {"message" : "CareerLens is working"}

#job retrieval and creation endpoints

@app.get("/jobs")
def get_jobs():
    response = supabase.table("jobs").select("*").execute()
    return response.data

@app.post("/jobs")
def create_job(job: Job):
    return save_job(job.model_dump())

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    response = (
        supabase
        .table("jobs")
        .select("*")
        .eq("id",job_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    return response.data[0]

#resume CRUD endpoints

@app.post("/upload-resume")
async def upload_resume(file:UploadFile):
    contents = await file.read()
    document = pymupdf.open(stream=contents, filetype="pdf")
    text =""
    for page in document:
        text+=page.get_text()
    result=extract_resume_data(text)
    saved_resume = save_resume(result)
    return saved_resume

class User(BaseModel):
    name:str

@app.post("/users")
def create_user(user:User):
    return [
        {"message":f"User {user.name} received."}
    ]

@app.get("/resumes")
def get_resumes():
    response = supabase.table("resumes").select('*').execute()
    return response

@app.get("/resumes/{resume_id}")
def get_resume(resume_id : str):
    response = (
        supabase
        .table("resumes")
        .select("*")
        .eq("id", resume_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="resume not found"
        )
    return response.data[0]

@app.delete("/resumes/{resume_id}")
def delete_resume(resume_id: str):
    response= (
        supabase
        .table("resumes")
        .delete()
        .eq("id",resume_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="resume not found"
        )
    return {"message":"Resume deleted successfully"}

@app.put("/resumes/{resume_id}")
def update_resume(
    resume_id: str,
    name: str | None = None,
    email: str | None = None,
    phone: str | None=None
):
    data={}
    if name is not None:
        data["name"]=name
    if email is not None:
        data["email"]=email
    if phone is not None:
        data["phone"]=phone
    if not data:
        raise HTTPException(
            status_code=404,
            detail="No fields provided for update"
        )
    response = (
        supabase
        .table("resumes")
        .update(data)
        .eq("id",resume_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )
    return response.data[0]

#MATCHING THE RESUME WITH JOBS AND RETURNING THE MATCH SCORE AND MISSING SKILLS

@app.post("/match/{resume_id}/{job_id}")
def match_resume_with_job(resume_id: str, job_id: str):

    # Get resume
    resume_response = (
        supabase
        .table("resumes")
        .select("*")
        .eq("id", resume_id)
        .execute()
    )

    if not resume_response.data:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    resume = resume_response.data[0]

    # Get job
    job_response = (
        supabase
        .table("jobs")
        .select("*")
        .eq("id", job_id)
        .execute()
    )

    if not job_response.data:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job = job_response.data[0]

    # Build structured resume evidence
    evidence = build_resume_evidence(resume)

    # Match every job requirement
    requirement_results = match_requirements(
        job["required_skills"],
        evidence
    )

    # Separate matched and missing requirements
    matched_skills = [
        result["requirement"]
        for result in requirement_results
        if result["matched"]
    ]

    missing_skills = [
        result["requirement"]
        for result in requirement_results
        if not result["matched"]
    ]

    # Calculate requirement-based match score
    total_requirements = len(requirement_results)

    if total_requirements:
        match_score = (
            len(matched_skills) / total_requirements
        ) * 100
    else:
        match_score = 0

    return {
        "resume_id": resume_id,
        "job_id": job_id,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2),
        "requirements": requirement_results
    }