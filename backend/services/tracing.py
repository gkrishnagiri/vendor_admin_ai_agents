from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 🔹 MAIN TRACE (API LEVEL)
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


# 🔹 CHILD SPAN (FOR LLM CALLS)
def start_span(trace, name: str):
    if trace is None:
        return None

    try:
        return client.beta.traces.spans.create(
            trace_id=trace.id,
            name=name
        )
    except Exception:
        return None


def end_span(span):
    if span is None:
        return

    try:
        client.beta.traces.spans.update(span.id, status="completed")
    except Exception:
        pass