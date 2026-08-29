import fitz
from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
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