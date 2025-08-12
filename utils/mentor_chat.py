from openai import OpenAI

client = OpenAI()

def generate_mentor_response(persona, query):
    prompt = f"""
You are acting as a {persona}. The user is seeking career-related advice.

User's Question:
{query}

Provide a detailed, helpful, encouraging, and professional response. 
Structure your answer clearly, and make it conversational if needed.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a career mentor AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content
    return content.strip() if content is not None else ""
