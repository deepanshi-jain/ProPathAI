import streamlit as st
from utils.mock_interview import generate_mock_interview
from utils.speech import speak_text
from utils.pdf_export import export_to_pdf

st.title("🧠 Interview Copilot")

role = st.text_input("Enter the job role:")
domain = st.text_input("Enter the domain (e.g., Data Science, Web Dev):")
num_questions = st.slider("How many questions?", 3, 10, 5)

if st.button("🎤 Generate Mock Interview"):
    with st.spinner("Generating..."):
        result = generate_mock_interview(role, domain, num_questions)
        st.session_state["mock_result"] = result
        st.text_area("🗣️ Interview Q&A", result, height=400)

if "mock_result" in st.session_state:
    if st.button("🔊 Read Aloud"):
        speak_text(st.session_state["mock_result"])

    if st.button("📄 Export to PDF"):
        file_path = export_to_pdf(st.session_state["mock_result"])
        with open(file_path, "rb") as f:
            st.download_button("📥 Download Interview", f, file_name="MockInterview.pdf")
