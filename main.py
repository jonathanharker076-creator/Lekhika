from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

class PromptRequest(BaseModel):
    prompt: str

SYSTEM_PROMPT = """
You are a professional Bengali writing assistant.

Your job is to write in natural, human Bengali that feels authored — not generated.

Follow these rules strictly:

1. Do not use template-based headings unless the topic requires structured sections.
2. Avoid generic examples unless necessary.
3. Avoid placeholders like “তথ্যসূত্র উল্লেখ করুন”.
4. Provide depth of reasoning.
5. Analyse both common and uncommon possibilities.
6. Maintain logical flow.
7. Avoid exaggeration.
8. If factual uncertainty exists, clearly mention limitation.
9. Avoid repetitive patterns.
10. Write like an educated Bengali columnist or researcher.

Tone:
Calm, analytical, thoughtful.

Structure:
Introduction → Core analysis → Broader implication → Conclusion.

Never sound mechanical.
Never sound like a generic AI.
"""

@app.post("/generate")
def refine_text(original_text):
    refinement_prompt = f"""
    Improve the following Bengali text:
    - Make it more natural.
    - Remove generic tone.
    - Strengthen logical flow.
    - Remove vague claims.
    - Make it feel human-written.

    Text:
    {original_text}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": refinement_prompt}],
            "temperature": 0.2
        }
    )

    return response.json()["choices"][0]["message"]["content"]

 @app.post("/generate")
def generate(data: PromptRequest):
    draft = generate_text(data.prompt)
    refined = refine_text(draft)
    return {"response": refined}

