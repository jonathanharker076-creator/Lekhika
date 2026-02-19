from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Read API key from Render environment variables
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# Personal style injection (edit this to match your tone)
USER_STYLE = """
The author writes in:
- Calm analytical tone
- Logical and structured reasoning
- Flowing paragraphs (avoid excessive bullet points)
- No emotional exaggeration
- Thoughtful, reflective depth
- No generic textbook formatting
"""

class PromptRequest(BaseModel):
    prompt: str


def generate_text(user_prompt: str):
    smart_prompt = f"""
Writing Style Guidelines:
{USER_STYLE}

Before writing, internally analyse:
- Core issue
- Hidden dimension
- Opposing perspective
- Practical implication
- Long-term consequence

Then write a refined Bengali article.

Rules:
- Do NOT use generic textbook headings.
- Avoid predictable structure.
- Avoid surface-level explanation.
- Maintain natural human Bengali.
- Strengthen reasoning.
- Avoid repetition.
- If factual uncertainty exists, clearly state limitation.
- Write like a thoughtful Bengali columnist.

Topic:
{user_prompt}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "user", "content": smart_prompt}
                ],
                "temperature": 0.35,
                "max_tokens": 800
            },
            timeout=20
        )

        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return f"Model error: {data}"

    except Exception as e:
        return f"System error: {str(e)}"


@app.post("/generate")
def generate(data: PromptRequest):
    result = generate_text(data.prompt)
    return {"response": result}
