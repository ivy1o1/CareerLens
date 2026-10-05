from matching.matcher import match_skills


resume_skills = [
    "Python",
    "FastAPI",
    "RESTful API development",
    "SQL",
    "Docker"
]

job_skills = [
    "python",
    "REST API",
    "PostgreSQL",
    "Graphic design"
]

results = match_skills(
    resume_skills,
    job_skills,
    threshold=0.6
)

for result in results:
    print("\nRequirement:", result["requirement"])
    print("Matched:", result["matched"])
    print("Match type:", result["match_type"])
    print("Matched skill:", result["matched_skill"])
    print("Similarity:", result["similarity"])