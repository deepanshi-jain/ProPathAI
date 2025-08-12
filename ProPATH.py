import streamlit as st
from streamlit_lottie import st_lottie
import requests

# --- Function to load Lottie animation ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Inject Custom CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Page config ---
st.set_page_config(page_title="ProPathAI", page_icon="🚀", layout="wide")

# --- Load Assets ---
lottie_career = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_tno6cg2w.json")

# --- Apply CSS ---
local_css("styles/chat.css")

# --- Sidebar Branding ---
with st.sidebar:
    st.markdown("## 🚀 ProPathAI")
    st.markdown("Your AI Career Assistant")
  
# --- Main Page Content ---
col1, col2 = st.columns([2, 3])

with col1:
    st_lottie(lottie_career, height=300, key="career")

with col2:
    st.title("🚀 ProPathAI – Your AI Career Assistant")
    st.markdown("Empowering your career journey with **AI-powered guidance**.")
    st.markdown("🔍 Analyze resumes, 🧑‍🏫 get mentorship, 💬 ace interviews, and plan your future.")

st.markdown("---")
st.subheader("📌 What You Can Do with ProPathAI")

features = [
    "📄 Resume Analyzer – Get ATS score & optimization tips",
    "✨ AI Resume Enhancer – Instantly rewrite and highlight improvements",
    "🧑‍🏫 Mentor Persona Chat – Ask career-specific questions to expert personas",
    "💬 Interview Copilot – Simulate adaptive interviews for any role",
    "📊 Recruiter Dashboard – Help recruiters easily browse, filter, and compare job descriptions and resume"
]

for feat in features:
    st.markdown(f"- {feat}")


