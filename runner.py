import os
from utils.io_utils import save_text, save_docx, ensure_dir
from generators.business import elaborate_idea, gen_business_docs
from generators.operations import gen_operations_docs
from generators.marketing import gen_marketing_docs
from generators.legal import gen_legal_docs
from generators.finance_docs import gen_finance_docs
from generators.market_docs import gen_market_docs
from intelligence.ai_auditor import audit_all
from intelligence.finance_model import simulate_revenue_monthly, fit_and_project
from intelligence.market_clustering import cluster_competitors
from intelligence.semantic_search import SemanticSearch

OUT = "data/generated"
# --- Add this function anywhere near the top ---
def ensure_sample_competitors_csv(path="data/sample_competitors.csv"):
    """Create a default competitors CSV if it's missing or empty."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        print("[⚙️] No competitor file found. Creating a sample file...")
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                "Company,Description,Country,Website\n"
                "Airbnb,Platform for booking unique stays and local experiences,USA,https://www.airbnb.com\n"
                "TripAdvisor,Travel reviews and destination guides,USA,https://www.tripadvisor.com\n"
                "Expedia,Online travel booking for flights hotels and packages,USA,https://www.expedia.com\n"
                "MakeMyTrip,Indian travel booking and holiday packages,India,https://www.makemytrip.com\n"
                "Goibibo,Online hotel and bus booking platform,India,https://www.goibibo.com\n"
                "Lonely Planet,Travel guide publisher and city explorer app,Australia,https://www.lonelyplanet.com\n"
                "Google Travel,AI powered travel planner with maps and itinerary suggestions,USA,https://www.google.com/travel\n"
            )
        print(f"[OK] Sample competitor CSV created at {path}")
    else:
        print(f"[✔] Competitor CSV already exists at {path}")

def main():
    ensure_dir(OUT)

    # 1) Put your starting idea here (or pass from CLI)
    idea = input("Enter your startup idea: ").strip() or "Uber for Personal Chefs"

    # 2) Elaborate
    elab = elaborate_idea(idea)
    save_text(elab, f"{OUT}/00_elaboration.txt")
    save_docx(elab, f"{OUT}/00_elaboration.docx")

    # 3) Generate all docs
    packs = [
        ("business", gen_business_docs(elab)),
        ("operations", gen_operations_docs(elab)),
        ("marketing", gen_marketing_docs(elab)),
        ("legal", gen_legal_docs(elab)),
        ("finance", gen_finance_docs(elab)),
        ("market", gen_market_docs(elab)),
    ]
    for folder, docs in packs:
        base = f"{OUT}/{folder}"
        ensure_dir(base)
        for name, content in docs.items():
            safe = name.replace("/", "_").replace(" ", "_")
            save_text(content, f"{base}/{safe}.txt")

    # 4) Build semantic search index
    ss = SemanticSearch()
    ss.build_from_folder(OUT)
    res = ss.query("What are my key revenue risks?", k=3)
    save_text(str(res), f"{OUT}/semantic_search_example.txt")

    # 5) Finance simulation & projection
    hist = simulate_revenue_monthly()
    proj, burn, plot = fit_and_project(hist, out_dir=OUT)
    hist.to_csv(f"{OUT}/historic_revenue.csv", index=False)
    proj.to_csv(f"{OUT}/projected_revenue.csv", index=False)

    # 6) Market clustering
    ensure_sample_competitors_csv("data/sample_competitors.csv")
    cluster_competitors(csv_path="data/sample_competitors.csv", out_dir=OUT)

    # 7) AI Consistency Audit
    audit = audit_all(folder=OUT)
    save_text(audit, f"{OUT}/ai_consistency_audit.txt")

    print("\nDone. See data/generated/ for outputs.")

if __name__ == "__main__":
    main()
