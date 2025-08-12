import streamlit as st
from utils.resume_parser import extract_text_from_pdf
from utils.resume_feedback import get_resume_feedback, get_ats_score

st.set_page_config(page_title="📄 Resume Analyzer")

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("🔍 Job Description")
    job_description = st.text_area("Paste the job description here:", height=200)

    if st.button("Analyze Resume & Get ATS Score"):
        with st.spinner("Analyzing your resume..."):
            feedback = get_resume_feedback(resume_text)
            ats_result = get_ats_score(resume_text, job_description)

            st.markdown("### 🧠 Resume Feedback")
            st.markdown(feedback)

            st.markdown("---")
            st.markdown("### 📊 ATS Compatibility Score")
            st.markdown(ats_result)

    # 🔁 Pass resume to enhancer module
    if st.button("✍️ Enhance Resume with AI"):
        st.session_state.resume_text = resume_text
        st.switch_page("pages/Resume_enhancer.py")  # path may vary
