import glob, os
from utils.openai_client import llm
from utils.prompts import AUDIT_PROMPT

def audit_all(folder="data/generated"):
    files = glob.glob(os.path.join(folder, "**/*.txt"), recursive=True)
    bundle = []
    for p in files:
        try:
            txt = open(p, "r", encoding="utf-8").read()
            name = os.path.relpath(p, folder)
            bundle.append(f"# {name}\n{txt}\n")
        except: pass
    joined = "\n\n".join(bundle)
    prompt = AUDIT_PROMPT.format(bundle=joined[:150000])  # keep prompt safe size
    return llm([{"role":"user","content":prompt}])
