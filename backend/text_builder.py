
def build_resume_text(resume: dict) -> str:
    parts = []

    # Education
    for education in resume["education"]:
        parts.append(
            f"Education: {education['degree']} at {education['institution']}. "
            f"Field of study: {education.get('field_of_study') or ''}"
        )

    # Skills
    parts.append(
        f"Technical skills: {', '.join(resume['skills']['technical'])}. "
        f"Tools: {', '.join(resume['skills']['tools'])}. "
        f"Soft skills: {', '.join(resume['skills']['soft'])}."
    )

    # Experience
    for experience in resume["experience"]:
        parts.append(
            f"Experience: {experience['role']} at {experience['company']}. "
            f"{experience.get('description') or ''}"
        )

    # Projects
    for project in resume["projects"]:
        parts.append(
            f"Project: {project['name']}. "
            f"{project['description']}. "
            f"Technologies: {project['technologies']}"
        )

    return "\n".join(parts)

def build_job_text(job: dict) -> str:
    parts = []

    parts.append(f"Job title: {job['title']}")
    parts.append(f"Description: {job.get('description') or ''}")
    parts.append(
        f"Required skills: {', '.join(job['required_skills'])}"
    )

    return "\n".join(parts)