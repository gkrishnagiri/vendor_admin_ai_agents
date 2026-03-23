from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def interpret_step(step: str):
    """
    Convert natural language step → structured browser action
    """

    prompt = f"""
You are an AI UI automation interpreter.

Convert the given instruction into a JSON action for browser automation.

---

SUPPORTED ACTIONS:

1. click
2. fill
3. navigate
4. wait

---

RULES:

- Use text-based selectors whenever possible
- Prefer: text=, placeholder=, label=
- Keep selectors simple and generic
- If filling, include "value"
- Output ONLY valid JSON

---

Examples:

Input: Click Users in sidebar
Output:
{{"action": "click", "selector": "text=Users"}}

Input: Enter username john123
Output:
{{"action": "fill", "selector": "input[placeholder='Username']", "value": "john123"}}

---

Instruction:
{step}

---

Output:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You convert UI steps into structured actions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        print("[Interpreter] Failed to parse JSON:", content)
        return {"action": "unknown"}