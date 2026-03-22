from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def plan_actions(query: str):
    """
    Convert user intent into step-by-step plan
    """

    prompt = f"""
You are an AI planning agent.

Your job is to break down a user's request into clear, ordered steps.

---

RULES:

- Output ONLY a list of steps
- Each step must be simple and actionable
- Do NOT execute anything
- Do NOT explain — only steps
- Keep steps generic (not tied to any specific UI unless mentioned)

---

User Request:
{query}

---

Output format (JSON array of steps):
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise planning agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content