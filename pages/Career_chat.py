import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create ChatOpenAI client
client = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Career Chatbot", page_icon="💬")
st.title("💬 Career Copilot Chatbot")

user_query = st.text_area("Ask your career-related question:", height=150)

if st.button("Get Answer") and user_query.strip():
    with st.spinner("Thinking..."):
        response = client([HumanMessage(content=user_query)])
        st.success(response.content)
       
