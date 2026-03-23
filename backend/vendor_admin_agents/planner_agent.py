from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def plan_actions(query: str):
    """
    Convert user intent into step-by-step plan
    """

    prompt = f"""
You are an AI planning agent.

Break down the user request into ordered UI steps.

---

RULES:

- Output ONLY JSON array
- Each step must be clear and actionable
- No explanations

---

User Request:
{query}

---

Output:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate structured plans."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        print("[Planner] Failed to parse JSON:", content)
        return []