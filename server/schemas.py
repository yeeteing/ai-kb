# Pydantic models define what our API expects and returns.
# They validate incoming JSON and help document the API.

from pydantic import BaseModel

class FAQIn(BaseModel):
    org_id: str
    question: str
    answer: str

class AskIn(BaseModel):
    org_id: str
    question: str

class AskOut(BaseModel):
    # Model the /ask response: the final answer, the supporting context snippets,
    # and latency breakdown in milliseconds (retrieve vs LLM vs total)
    answer: str
    context: list[dict]
    latency_ms: dict