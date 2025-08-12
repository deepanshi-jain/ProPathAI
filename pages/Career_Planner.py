import streamlit as st
from utils.resume_parser import extract_text_from_pdf
from utils.career_planner import generate_career_plan

st.set_page_config(page_title="Career Planner", page_icon="🧠")
st.title("🧠 Career Plan")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)

    goal = st.text_input("What is your dream job title? (e.g., Data Scientist, ML Engineer)")

    if st.button("Generate Career Plan"):
        with st.spinner("Analyzing your resume and building a personalized career path..."):
            plan = generate_career_plan(resume_text, goal)
            st.markdown("### 📈 Your Career Roadmap")
            st.markdown(plan)
