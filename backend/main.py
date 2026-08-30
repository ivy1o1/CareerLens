import pymupdf
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
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
    document = pymupdf.open(stream=contents, filetype="pdf")
    text =""
    for page in document:
        text+=page.get_text()
    result=extract_resume_data(text)
    return result

class User(BaseModel):
    name:str

@app.post("/users")
def create_user(user:User):
    return [
        {"message":f"User {user.name} received."}
    ]


class Education(BaseModel):
    degree:str
    institution: str
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    gpa: str | None = None

class Experience(BaseModel):
    role: str
    company: str
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None

class Project(BaseModel):
    name: str
    description: str
    technologies: str

class Certification(BaseModel):
    name: str
    issuer: str | None = None
    date: str | None = None

class Achievement(BaseModel):
    title: str
    description: str | None = None

class PersonalInfo(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None

class Resume(BaseModel):
    personal_info: PersonalInfo
    education: list[Education]
    skills: list[str]
    experience:list[Experience]
    projects: list[Project]
    certifications: list[Certification]
    achievements: list[Achievement]


load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
print("API key found:", api_key is not None)
client = genai.Client(api_key=api_key)

def extract_resume_data(text:str):
    prompt = f"""
    Extract the information from this resume.

    Resume text:
    {text}
    """
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type":"application/json",
        "response_schema": Resume,
    })
    return response.parsed

