import pymupdf
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
from database import supabase
from database import save_resume
from fastapi import HTTPException
from models import(
    Resume,
)
from resume_parser import extract_resume_data
app = FastAPI()

@app.get("/")
def home():
    return {"message" : "CareerLens is working"}

@app.get("/jobs")
def get_jobs():
    return [
        {"title":"AI/ML Intern", "company":"Example Corp"},
        {"title":"Backend Intern","company":"Tech company"}
    ]

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