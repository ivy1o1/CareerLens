import pymupdf
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
from database import save_job, supabase, save_resume
from fastapi import HTTPException
from models import(
    Resume,
    Job
)
from resume_parser import extract_resume_data
from text_builder import build_resume_text, build_job_text
from embeddings import get_embedding, cosine_similarity

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
    resume_response =(
        supabase
        .table("resumes")
        .select("*")
        .eq("id",resume_id)
        .execute()
    )
    if not resume_response.data:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )
    resume = resume_response.data[0]

    job_response = (
        supabase
        .table("jobs")
        .select("*")
        .eq("id",job_id)
        .execute()
    )
    if not job_response.data:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    job = job_response.data[0]
    
    resume_text = build_resume_text(resume)
    job_text = build_job_text(job)

    resume_embedding = get_embedding(resume_text)
    job_embedding = get_embedding(job_text)

    semantic_similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )
    semantic_score =semantic_similarity * 100

    resume_skills = resume["skills"]["technical"] + resume["skills"]["tools"] + resume["skills"]["soft"]
    norm_res_skills = set()
    for skill in resume_skills:
        norm_res_skills.add(skill.lower().strip())

    required_skills = job["required_skills"]
    norm_job_skills = set()
    for skill in required_skills:
        norm_job_skills.add(skill.lower().strip())

    matched_skills = norm_res_skills.intersection(norm_job_skills)
    missing_skills = norm_job_skills.difference(norm_res_skills)

    if norm_job_skills:
        match_score =(len(matched_skills) / len(norm_job_skills))* 100
    else:
        match_score = 0

    return {
        "resume_id": resume_id,
        "job_id": job_id,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_score": round(match_score,2),
        "semantic_score": round(semantic_score, 2)
    }