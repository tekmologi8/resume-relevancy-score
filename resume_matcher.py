def match_resume_to_job(resume_text, job_desc, custom_skills=None):
    score = 0
    resume_text = resume_text.lower()
    job_desc = job_desc.lower()
    
    skills = custom_skills or []
    if not skills:
        with open("skills.txt") as f:
            skills = [line.strip().lower() for line in f]

    match_count = sum(1 for skill in skills if skill in resume_text and skill in job_desc)
    score = (match_count / len(skills)) * 100 if skills else 0
    return score
