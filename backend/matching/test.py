from matching.evidence import build_resume_evidence
from matching.matcher import match_requirement


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
    result = match_requirement(
        requirement,
        evidence,
        threshold=0.6
    )

    print("\nRequirement:", result["requirement"])
    print("Matched:", result["matched"])
    print("Match type:", result["match_type"])
    print("Similarity:", result["similarity"])
    print("Evidence:", result["evidence"])