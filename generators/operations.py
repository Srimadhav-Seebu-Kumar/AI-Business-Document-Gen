from utils.openai_client import llm
from utils.prompts import DOCS_PROMPT

def gen_operations_docs(idea_elab: str) -> dict:
    titles = [
        "Organizational Structure / Org Chart",
        "Hiring Plan",
        "Standard Operating Procedures (SOPs)",
        "Product/Service Roadmap",
        "Product Requirement Document (PRD)",
        "Technology Stack & Infrastructure Plan",
    ]
    out = {}
    for t in titles:
        out[t] = llm([{"role":"user","content":DOCS_PROMPT.format(idea=idea_elab, title=t)}])
    return out
