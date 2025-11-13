from utils.openai_client import llm
from utils.prompts import DOCS_PROMPT

def gen_market_docs(idea_elab: str) -> dict:
    titles = [
        "Market Analysis",
        "Customer Persona Sheets",
        "Competitor Analysis",
        "Product-Market Fit Analysis",
        "Regulatory/Compliance Overview",
    ]
    return {t: llm([{"role":"user","content":DOCS_PROMPT.format(idea=idea_elab, title=t)}]) for t in titles}
