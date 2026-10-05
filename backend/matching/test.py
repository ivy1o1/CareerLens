from matching.evidence import build_resume_evidence
from matching.matcher import retrieve_evidence
from matching.evaluator import evaluate_requirement

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

    retrieved = retrieve_evidence(
        requirement,
        evidence,
        top_k=3
    )

    result = evaluate_requirement(
        requirement,
        retrieved
    )

    print("\nRequirement:", requirement)

    print("Retrieved evidence:")
    for item in retrieved:
        print(
            item["similarity"],
            "|",
            item["match_type"],
            "|",
            item["evidence"]["text"]
        )

    print("LLM evaluation:")
    print(result)