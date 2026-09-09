import pymupdf
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
from database import save_resume
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





