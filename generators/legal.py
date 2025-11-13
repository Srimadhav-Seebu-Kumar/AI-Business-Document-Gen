from utils.openai_client import llm
from utils.prompts import DOCS_PROMPT

def gen_legal_docs(idea_elab: str) -> dict:
    titles = [
        "Articles of Incorporation",
        "Founder’s Agreement / Partnership Agreement",
        "Intellectual Property (IP) Summary",
        "Privacy Policy / Terms of Service",
        "Vendor Contracts",
        "NDAs / MOUs",
    ]
    return {t: llm([{"role":"user","content":DOCS_PROMPT.format(idea=idea_elab, title=t)}]) for t in titles}
