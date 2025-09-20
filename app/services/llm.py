# Wraps the LLM call. If there's no API key, return a small demo answer,
# so the pipeline still "works" during setup or interviews.

from app.config import settings

SYSTEM_PROMPT = (
    "You are a helpful support assistant. Answer ONLY using the provided context. "
    "If the answer is not in the context, say 'I don't know'. Keep answers short."
)

def build_prompt(context_snips: list[str], question: str) -> str:
    # Construct a simple prompt: strict instruction + context + question
    joined = "\n\n".join(context_snips) if context_snips else "(no context)"
    return f"{SYSTEM_PROMPT}\n\nContext:\n{joined}\n\nQuestion: {question}\nAnswer:"

async def answer_with_llm(context_snips: list[str], question: str) -> str:
    # If no OpenAI key is set, just return a placeholder so the demo runs
    if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
        return "(demo) Based on the context, here’s the best answer I can provide."

    # OpenAI path (you can add Anthropic/Azure branches later)
    if settings.LLM_PROVIDER == "openai":
        import openai
        openai.api_key = settings.OPENAI_API_KEY
        prompt = build_prompt(context_snips, question)

        # Call a small, f7ast model (adjust to what you have access to)
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,   # low temperature = more deterministic answers
        )
        return resp.choices[0].message.content.strip()

    # If provider isn't supported
    raise ValueError("Unsupported LLM provider or missing API key.")
