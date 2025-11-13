from utils.openai_client import llm
from utils.prompts import DOCS_PROMPT

def gen_marketing_docs(idea_elab: str) -> dict:
    titles = [
        "Marketing Plan",
        "Sales Strategy",
        "Go-To-Market (GTM) Plan",
        "Brand Identity Guide",
        "Customer Journey Map",
    ]
    return {t: llm([{"role":"user","content":DOCS_PROMPT.format(idea=idea_elab, title=t)}]) for t in titles}
