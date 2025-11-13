BUSINESS_ELABORATION = """You are a startup strategist.
Elaborate clearly on this idea:
"{idea}"

Include:
1) Business Concept
2) Target Audience
3) Key Features / Offerings
4) Unique Value Proposition
5) Revenue Model
6) Delivery Channels
7) Scalability Potential
8) Early Challenges
"""

DOCS_PROMPT = """Using the elaborated idea below, generate the following document.
Write clearly with headings:
---
{idea}
---
Now produce: {title}
"""

AUDIT_PROMPT = """You are an AI business auditor.
Given these documents, find inconsistencies, missing numbers, or contradictions.
Output sections:
1) Summary
2) Inconsistencies (with references)
3) Conflicts across documents
4) Risks & Recommendations

DOCUMENTS:
{bundle}
"""

TONE_REWRITE_PROMPT = """You are a copy editor.
Rewrite the text to match the desired tone: {tone}.
Preserve facts, improve clarity, keep similar length.

TEXT:
{content}
"""
