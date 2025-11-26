import glob, os
from utils.openai_client import llm
from utils.prompts import AUDIT_PROMPT

import os
import glob
from utils.openai_client import llm

MAX_CHARS = 8000      # hard limit so we never exceed token window
MAX_FILES = 5         # limit how many docs we audit

def audit_all(folder):
    files = sorted(
        glob.glob(os.path.join(folder, "**/*.txt"), recursive=True),
        key=os.path.getmtime,
        reverse=True
    )[:MAX_FILES]

    combined = ""
    total_len = 0

    for f in files:
        text = open(f, "r", encoding="utf-8").read()
        if (total_len + len(text)) > MAX_CHARS:
            break
        combined += f"\n\n### FILE: {os.path.basename(f)}\n{text}"
        total_len += len(text)

    prompt = f"""
You are an AI document auditor.

Analyze the following documents for:
- contradictions
- missing info
- repeated info
- inconsistencies in terminology
- gaps in logic
- unclear assumptions

Documents:
{combined}

Provide a structured audit summary.
"""

    return llm([{"role": "user", "content": prompt}])

