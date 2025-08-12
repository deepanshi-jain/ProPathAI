import streamlit as st
import fitz  # PyMuPDF
import openai
from openai import OpenAI

st.set_page_config(page_title="📝 AI Resume Enhancer")

st.title("📝 AI Resume Enhancer")
st.markdown("Enhance your resume using AI for better job alignment.")

# Function to extract text if file is uploaded (optional fallback)
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# 🧠 Use resume text from session or uploaded file
resume_text = st.session_state.get("resume_text", "")
if not resume_text:
    uploaded_file = st.file_uploader("Or upload your resume (PDF)", type=["pdf"])
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)

if resume_text:
    st.subheader("📄 Extracted Resume Text")
    st.text_area("Here is your resume:", resume_text, height=300)

    if st.button("🔧 Enhance My Resume"):
        with st.spinner("Enhancing your resume..."):
            prompt = f"""Improve the following resume to align better with modern ATS systems and recruiter expectations.
Highlight impact, skills, and make it concise and professional.

RESUME:
{resume_text}
"""
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            content = response.choices[0].message.content
            enhanced_resume = content.strip() if content is not None else ""

        st.subheader("🚀 Enhanced Resume")
        st.text_area("Here is your AI-enhanced resume:", enhanced_resume, height=400)

        # Optional download
        st.download_button("📥 Download Enhanced Resume", enhanced_resume, file_name="enhanced_resume.txt")
