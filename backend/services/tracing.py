from openai import OpenAI
import os
from dotenv import load_dotenv

# 🔥 LOAD ENV
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def start_trace(name: str):
    try:
        return client.beta.traces.create(name=name)
    except Exception:
        return None


def end_trace(trace):
    if trace is None:
        return

    try:
        client.beta.traces.update(trace.id, status="completed")
    except Exception:
        pass