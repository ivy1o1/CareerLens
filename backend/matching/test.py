from matching.evidence import build_resume_evidence
from matching.matcher import retrieve_evidence


resume = {
    "skills": {
        "technical": ["Python", "FastAPI", "SQL"],
        "tools": ["Docker", "Git"]
    },
    "experience": [
        {
            "role": "Backend Intern",
            "company": "ABC",
            "description": "Built REST APIs using FastAPI and Python."
        }
    ],
    "projects": [
        {
            "name": "CareerLens",
            "description": "Built a job matching platform.",
            "technologies": ["Python", "FastAPI", "Supabase"]
        }
    ],
    "education": [
        {
            "degree": "B.Tech",
            "institution": "NSUT",
            "field_of_study": "Information Technology"
        }
    ]
}


evidence = build_resume_evidence(resume)

requirements = [
    "Python",
    "REST API",
    "PostgreSQL",
    "Graphic design"
]

for requirement in requirements:
    results = retrieve_evidence(
        requirement,
        evidence,
        top_k=3
    )

    print("\nRequirement:", requirement)

    for result in results:
        print(
            result["similarity"],
            "|",
            result["match_type"],
            "|",
            result["evidence"]["text"]
        )