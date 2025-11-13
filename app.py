import streamlit as st
import os, glob, pandas as pd
from utils.io_utils import load_text
from generators.business import elaborate_idea
from intelligence.semantic_search import SemanticSearch
from intelligence.ai_auditor import audit_all
from intelligence.finance_model import simulate_revenue_monthly, fit_and_project
from intelligence.market_clustering import cluster_competitors
from intelligence.sentiment_tone import analyze_sentiment, rewrite_tone

OUT = "data/generated"

st.set_page_config(page_title="AI Startup Suite", layout="wide")
st.title("🚀 AI Startup Suite")

# Input
idea = st.text_area("Your startup idea", placeholder="e.g., platform that provides local travel guides and maps for various cities and destinations around the world.", height=100)
colA, colB = st.columns(2)
with colA:
    if st.button("Elaborate Idea & Generate Core Docs"):
        os.makedirs(OUT, exist_ok=True)
        elab = elaborate_idea(idea or "Uber for Personal Chefs")
        open(f"{OUT}/00_elaboration.txt","w",encoding="utf-8").write(elab)
        st.success("Elaboration saved. Run `runner.py` for full pack, or use tools below.")

with colB:
    if st.button("Run AI Consistency Audit"):
        audit = audit_all(folder=OUT)
        st.session_state["audit"] = audit
        st.success("Audit complete.")
        st.download_button("Download Audit", data=audit, file_name="ai_consistency_audit.txt")

st.header("📄 Browse Generated Docs")
files = glob.glob(os.path.join(OUT, "**/*.txt"), recursive=True)
sel = st.selectbox("Select a file", options=["--"] + files)
if sel and sel != "--":
    st.code(load_text(sel)[:20000])

st.header("🔎 Semantic Search")
q = st.text_input("Ask across all documents", value="What are my key revenue risks?")
if st.button("Search"):
    ss = SemanticSearch()
    ss.build_from_folder(OUT)
    rs = ss.query(q, k=5)
    for r in rs:
        st.write(f"**{r['path']}** (score={r['score']:.4f})")
        st.code(r["snippet"])

st.header("📈 Finance Projection")
if st.button("Simulate & Project"):
    hist = simulate_revenue_monthly()
    proj, burn, plot = fit_and_project(hist, out_dir=OUT)
    st.write("Average monthly burn (est.):", round(burn,2))
    st.line_chart(hist.set_index("month"))
    st.line_chart(proj.set_index("month"))
    if os.path.exists(plot):
        st.image(plot)
    st.success("Finance charts updated.")

st.header("🏷️ Competitor Clustering")
k = st.slider("Clusters (k)", 2, 6, 3)
if st.button("Cluster Now"):
    df, plot = cluster_competitors(k=k)
    st.dataframe(df)
    if plot and os.path.exists(plot):
        st.image(plot)

st.header("🙂 Sentiment & Tone")
text = st.text_area("Paste marketing copy to analyze & rewrite")
tone = st.selectbox("Desired tone", ["persuasive", "formal", "friendly", "authoritative"])
c1,c2 = st.columns(2)
with c1:
    if st.button("Analyze sentiment"):
        if text.strip():
            st.json(analyze_sentiment(text))
with c2:
    if st.button("Rewrite tone"):
        if text.strip():
            out = rewrite_tone(text, tone=tone)
            st.code(out)
