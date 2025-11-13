from utils.openai_client import llm
from utils.prompts import DOCS_PROMPT

def gen_finance_docs(idea_elab: str) -> dict:
    titles = [
        "Financial Plan / Forecast",
        "Budget Breakdown",
        "Cash Flow Statement",
        "Balance Sheet",
        "Income Statement",
        "Unit Economics",
        "Pricing Strategy Document",
        "Pitch Deck",
        "One-Pager / Teaser",
        "Funding Strategy",
        "Cap Table",
        "Term Sheet",
        "Use of Funds Breakdown",
    ]
    return {t: llm([{"role":"user","content":DOCS_PROMPT.format(idea=idea_elab, title=t)}]) for t in titles}
