from utils.openai_client import llm
from utils.prompts import BUSINESS_ELABORATION, DOCS_PROMPT

def elaborate_idea(idea: str) -> str:
    prompt = BUSINESS_ELABORATION.format(idea=idea)
    return llm([{"role":"user","content":prompt}])

def gen_business_docs(idea_elab: str) -> dict:
    titles = [
        "Executive Summary",
        "Business Plan",
        "Vision & Mission Statement",
        "Company Profile",
    ]
    out = {}
    for t in titles:
        prompt = DOCS_PROMPT.format(idea=idea_elab, title=t)
        out[t] = llm([{"role":"user","content":prompt}])
    return out
