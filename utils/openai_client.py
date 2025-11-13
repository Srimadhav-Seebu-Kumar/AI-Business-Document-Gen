import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

def llm(messages, model: str = MODEL, temperature: float = 0.2):
    resp = _client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content

def embed_texts(texts, model: str = EMBED_MODEL):
    # returns list of vectors
    resp = _client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]
