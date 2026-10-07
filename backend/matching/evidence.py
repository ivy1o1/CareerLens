def build_resume_evidence(resume: dict) -> list[dict]:
    evidence = []

    # Skills
    skills = resume.get("skills", {})

    for skill in skills.get("technical", []):
        evidence.append({
            "source_type": "skill",
            "text": skill,
            "source_name": None
        })

    for tool in skills.get("tools", []):
        evidence.append({
            "source_type": "tool",
            "text": tool,
            "source_name": None
        })
        for skill in skills.get("soft", []):
            evidence.append({
            "source_type": "soft_skill",
            "text": skill,
            "source_name": None
        })
        

    # Experience
    for experience in resume.get("experience", []):
        role = experience.get("role", "")
        company = experience.get("company", "")
        description = experience.get("description") or ""

        if description:
            evidence.append({
                "source_type": "experience",
                "text": description,
                "source_name": f"{role} at {company}"
            })

    # Projects
    for project in resume.get("projects", []):
        project_name = project.get("name", "")
        description = project.get("description") or ""

        if description:
            evidence.append({
                "source_type": "project",
                "text": description,
                "source_name": project_name
            })

        for technology in project.get("technologies", []):
            evidence.append({
                "source_type": "project_technology",
                "text": technology,
                "source_name": project_name
            })
            
    # Certifications
    for certification in resume.get("certifications", []):
        name = certification.get("name", "")
        issuer = certification.get("issuer") or ""

        if name:
            evidence.append({
                "source_type": "certification",
                "text": name,
                "source_name": issuer
            })
            
    # Achievements
    for achievement in resume.get("achievements", []):
        title = achievement.get("title", "")
        description = achievement.get("description") or ""

        text = f"{title}: {description}".strip(": ")

        if text:
            evidence.append({
                "source_type": "achievement",
                "text": text,
                "source_name": None
            })

    # Education
    for education in resume.get("education", []):
        degree = education.get("degree", "")
        institution = education.get("institution", "")
        field = education.get("field_of_study") or ""

        text = f"{degree} {field}".strip()

        if text:
            evidence.append({
                "source_type": "education",
                "text": text,
                "source_name": institution
            })

    return evidence