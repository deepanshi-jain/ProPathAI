import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_career_plan(resume_text, goal):
    prompt = f"""
You are a Career Planning Assistant.

Based on the resume below and the user's desired job title "{goal}", provide:
1. Key strengths that align with the role.
2. Gaps or missing skills.
3. Courses or certifications to fill those gaps.
4. A 3-step career roadmap to reach the goal.
5. Suggested LinkedIn headline for that goal.

RESUME:
{resume_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        return content.strip() if content is not None else ""
    except Exception as e:
        return f"Error: {str(e)}"
