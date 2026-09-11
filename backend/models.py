from pydantic import BaseModel
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

class Skills(BaseModel):
    technical: list[str]
    tools: list[str]
    soft: list[str]

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
    skills: Skills
    experience:list[Experience]
    projects: list[Project]
    certifications: list[Certification]
    achievements: list[Achievement]

class Job(BaseModel):
    title: str
    company: str
    description: str | None = None
    required_skills: list[str] = []
    location: str | None = None
    job_type: str | None = None
    application_url: str | None = None