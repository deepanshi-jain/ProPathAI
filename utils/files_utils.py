import json
import streamlit as st

# Load the JSON file
with open("data/candidate.json") as f:
    entries = json.load(f)

# Separate job descriptions and resumes
job_descriptions = [e for e in entries if e["type"] == "job_description"]
resume_examples = [e for e in entries if e["type"] == "resume_example"]
