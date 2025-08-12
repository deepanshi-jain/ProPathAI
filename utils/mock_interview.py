import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_mock_interview(role, domain, num_questions=5):
    prompt = f"""
    Generate a mock interview with {num_questions} questions and answers for a {role} role in {domain}. 
    Format:
    Q1: ...
    A1: ...
    Q2: ...
    A2: ...
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        return content.strip() if content is not None else ""
    except Exception as e:
        return f"Error: {str(e)}"
