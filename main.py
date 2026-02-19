from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

class PromptRequest(BaseModel):
    prompt: str

SYSTEM_PROMPT = """
You are a Bengali Writing Assistant.
Write in natural human Bengali.
Be structured and clear.
Avoid hallucination.
If uncertain, mention limitation.
Respond logically.
"""

@app.post("/generate")
def generate(data: PromptRequest):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": data.prompt}
            ],
            "temperature": 0.4
        }
    )

    return {
        "response": response.json()["choices"][0]["message"]["content"]
    }
