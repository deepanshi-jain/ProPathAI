from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_resume_feedback(resume_text):
    """Generate feedback for a given resume"""
    prompt = f"""
You are a professional career coach and resume reviewer.

I have uploaded my resume. Please provide:
1. A brief critique.
2. 3 suggestions to improve.
3. Whether it's suitable for data analyst or AI/ML roles.
4. Identify any missing key skills or weak points.

Resume Text:
{resume_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        return content.strip() if content is not None else ""
    except Exception as e:
        return f"Error: {str(e)}"

def get_ats_score(resume_text, job_description):
    """Simulate ATS scoring for resume vs job description"""
    prompt = f"""
You are an ATS (Applicant Tracking System) simulator.

Evaluate the following resume against this job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return the following:
1. ATS Score out of 100
2. Matched keywords
3. Missing important keywords
4. Formatting issues (tables, missing headers, contact info)
5. Final verdict: Pass / Borderline / Fail
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content
        return content.strip() if content is not None else ""
    except Exception as e:
        return f"Error: {str(e)}"
