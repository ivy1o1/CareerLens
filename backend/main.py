import fitz
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
import os
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
    document = fitz.open(stream=contents, filetype="pdf")
    text =""
    for page in document:
        text+=page.get_text()
    return {"text":text}

class User(BaseModel):
    name:str

@app.post("/users")
def create_user(user:User):
    return [
        {"message":f"User {user.name} received."}
    ]


class Education(BAseModel):
    degree:str
    institution: str
    major = str
    start_date: str
    end_date: str
    gpa: str

class Experience(BaseModel):
    role: str
    company: str
    start_date: str
    end_date: str
    description: str

class Project(BaseModel):
    name: str
    description: str
    technologies: str

class Certifications(BaseModel):
    name: str
    issuer: str
    date: str

class Achievements(BaseModel):
    title: str
    description: str

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str

class Resume(BaseModel):
    personal_info: PersonalInfo
    educaion: list[Education]
    skills: list[str]
    experience:list[Experience]
    projects: list[Project]
    certifications: list[Certifications]
    achievements: list[Achievements]

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")