import streamlit as st
from utils.mentor_chat import generate_mentor_response

st.title("🧑‍🏫 Mentor Copilot")

# Let user type the mentor persona
persona = st.text_input("Enter the mentor persona (e.g., Career Coach, Tech Lead, HR Recruiter):")

# Let user type their question
user_question = st.text_area("Ask your question:")

# Generate response
if st.button("Get Mentor Advice"):
    if persona.strip() == "" or user_question.strip() == "":
        st.warning("Please enter both a persona and a question.")
    else:
        response = generate_mentor_response(persona, user_question)
        st.markdown("### 💬 Mentor's Advice")
        st.write(response)
