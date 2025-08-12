import streamlit as st
import json

# Load recruiter data (JSON)
with open("data/candidate.json") as f:
    entries = json.load(f)

# Separate entries into job descriptions and resumes
job_descriptions = [e for e in entries if e["type"] == "job_description"]
resume_examples = [e for e in entries if e["type"] == "resume_example"]

st.set_page_config(page_title="Recruiter Dashboard", layout="wide")

st.title("🧑‍💼 Recruiter Dashboard")

# --------------- Job Descriptions -----------------
st.subheader("📌 Job Descriptions")

# 🔍 Filters for Job Descriptions
exp_levels = list(set([job["experience_level"] for job in job_descriptions]))
selected_level = st.selectbox("Filter by Experience Level", ["All"] + exp_levels)
skill_filter = st.text_input("Search by Skill (e.g., Python, SQL)")

# Apply filtering
filtered_jobs = job_descriptions
if selected_level != "All":
    filtered_jobs = [job for job in filtered_jobs if job["experience_level"] == selected_level]
if skill_filter:
    filtered_jobs = [
        job for job in filtered_jobs
        if any(skill_filter.lower() in skill.lower() for skill in job["skills"])
    ]

# Display job descriptions
if filtered_jobs:
    for job in filtered_jobs:
        st.markdown(f"### {job['title']}")
        st.write(f"**Company:** {job['company']}")
        st.write(f"**Skills:** {', '.join(job['skills'])}")
        st.write(f"**Level:** {job['experience_level']}")
        st.markdown("---")
else:
    st.warning("No job descriptions match your filters.")

# --------------- Resume Examples -----------------
st.subheader("📄 Resume Examples")

# Filters for Resume Examples
resume_skill_filter = st.text_input("Search Resume by Skill")
min_experience = st.slider("Minimum Experience (Years)", 0, 10, 0)

filtered_resumes = [
    resume for resume in resume_examples
    if resume["experience_years"] >= min_experience and
       (resume_skill_filter.lower() in " ".join(resume["skills"]).lower() if resume_skill_filter else True)
]

if filtered_resumes:
    for resume in filtered_resumes:
        st.markdown(f"### {resume['title']}")
        st.write(f"**Experience:** {resume['experience_years']} years")
        st.write(f"**Skills:** {', '.join(resume['skills'])}")
        st.write(f"**Success Rate:** {resume['success_rate']}")
        st.markdown("---")
else:
    st.warning("No resumes match your filters.")
