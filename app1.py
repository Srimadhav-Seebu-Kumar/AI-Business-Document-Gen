import streamlit as st
import os, glob, pandas as pd

from utils.io_utils import load_text
from generators.business import elaborate_idea
from intelligence.semantic_search import SemanticSearch
from intelligence.ai_auditor import audit_all
from intelligence.finance_model import simulate_revenue_monthly, fit_and_project
from intelligence.market_clustering import cluster_competitors
from intelligence.sentiment_tone import analyze_sentiment, rewrite_tone

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
OUT = "data/generated"
st.set_page_config(page_title="AI Startup Suite", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-size: 36px !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
    }
    .section-title {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #2e2e2e !important;
        margin-top: 35px !important;
    }
    .preview-box {
        background-color: #f2f2f2 !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
        padding: 15px !important;
        height: 450px !important;
        overflow-y: auto !important;
        white-space: pre-wrap !important;
        font-family: "Courier New", monospace !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Startup Suite</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# IDEA INPUT
# ---------------------------------------------------------------------------
st.subheader("Input Idea")
idea = st.text_area(
    "Describe your startup concept",
    placeholder="e.g., Platform for local travel guides customized for each city.",
    height=120
)

colA, colB = st.columns(2)
with colA:
    if st.button("Generate Core Documents"):
        os.makedirs(OUT, exist_ok=True)
        elab = elaborate_idea(idea or "Uber for Personal Chefs")
        open(f"{OUT}/00_elaboration.txt", "w", encoding="utf-8").write(elab)
        st.success("Base elaboration generated.")

with colB:
    if st.button("Run AI Consistency Audit"):
        audit = audit_all(folder=OUT)
        st.session_state["audit"] = audit
        st.download_button("Download Audit", data=audit, file_name="ai_consistency_audit.txt")
        st.success("Audit complete.")

# ---------------------------------------------------------------------------
# GENERATED DOCS BROWSER WITH LIVE PREVIEW
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Generated Documents</div>', unsafe_allow_html=True)

files = sorted(glob.glob(os.path.join(OUT, "**/*.txt"), recursive=True))
selected_doc = st.selectbox("Select document to preview", ["-- Select --"] + files)

if selected_doc and selected_doc != "-- Select --":
    content = load_text(selected_doc)
    st.markdown("**Preview:**")
    st.markdown(f'<div class="preview-box">{content}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TABS FOR FEATURES
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Tools & Analysis</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Semantic Search",
    "Finance Projection",
    "Competitor Clustering",
    "Sentiment & Tone"
])

# ---------------------------------------------------------------------------
# TAB 1 — SEMANTIC SEARCH
# ---------------------------------------------------------------------------
with tab1:
    st.write("Search across all documents using vector embeddings.")
    q = st.text_input("Query", placeholder="e.g., What are my revenue risks?")
    if st.button("Run Search"):
        ss = SemanticSearch()
        ss.build_from_folder(OUT)
        results = ss.query(q, k=5)
        for r in results:
            st.markdown(f"**Source:** {r['path']} — Score {r['score']:.3f}")
            st.markdown(f'<div class="preview-box">{r["snippet"]}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 2 — FINANCE PROJECTION
# ---------------------------------------------------------------------------
with tab2:
    if st.button("Simulate & Project Financials"):
        hist = simulate_revenue_monthly()

        # CORRECTED ARG ORDER
        proj, burn, plot = fit_and_project(hist, out_dir=OUT)

        st.metric("Estimated Monthly Burn", f"${burn:,.2f}")
        st.line_chart(hist.set_index("month"))
        st.line_chart(proj.set_index("month"))

        if os.path.exists(plot):
            st.image(plot)


# ---------------------------------------------------------------------------
# TAB 3 — COMPETITOR CLUSTERING
# ---------------------------------------------------------------------------
with tab3:
    k = st.slider("Number of clusters", 2, 8, 3)
    if st.button("Cluster Competitors"):
        df, plot = cluster_competitors(k=k)
        st.dataframe(df, use_container_width=True)
        if plot and os.path.exists(plot):
            st.image(plot)

# ---------------------------------------------------------------------------
# TAB 4 — SENTIMENT & TONE
# ---------------------------------------------------------------------------
with tab4:
    text = st.text_area("Paste marketing content")
    tone = st.selectbox("Rewrite tone", ["persuasive", "formal", "friendly", "authoritative"])

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Analyze Sentiment"):
            if text.strip():
                st.json(analyze_sentiment(text))

    with c2:
        if st.button("Rewrite Text"):
            if text.strip():
                out = rewrite_tone(text, tone=tone)
                st.markdown(f'<div class="preview-box">{out}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# EXTRA FEATURES ADDED
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Additional Tools</div>', unsafe_allow_html=True)

extra_col1, extra_col2 = st.columns(2)

# 🔍 NEW: Quick Doc Downloader
with extra_col1:
    st.write("Download all generated documents as a ZIP for offline use.")
    if st.button("Build ZIP Package"):
        import shutil
        zip_path = "generated_bundle.zip"
        shutil.make_archive("generated_bundle", "zip", OUT)
        with open(zip_path, "rb") as f:
            st.download_button("Download ZIP", f, file_name="startup_documents.zip")

# 📊 NEW: Document Stats
with extra_col2:
    st.write("Quick statistics for generated files")
    if files:
        stats = []
        for f in files:
            size_kb = os.path.getsize(f) / 1024
            stats.append([os.path.basename(f), f"{size_kb:.1f} KB"])
        st.table(pd.DataFrame(stats, columns=["Document", "Size"]))
