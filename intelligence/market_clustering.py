import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def cluster_competitors(csv_path="data/sample_competitors.csv", out_dir="data/generated", k=3):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    if "Description" not in df.columns:
        raise ValueError("CSV must contain a 'Description' column.")

    tfidf = TfidfVectorizer(stop_words="english", max_features=300)
    X = tfidf.fit_transform(df["Description"].fillna(""))

    Xs = StandardScaler(with_mean=False).fit_transform(X)
    k = min(k, len(df))
    km = KMeans(n_clusters=k, random_state=42)
    labels = km.fit_predict(Xs)
    df["Cluster"] = labels

    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X.toarray())
    df["PCA1"], df["PCA2"] = coords[:, 0], coords[:, 1]

    plt.figure(figsize=(8, 6))
    plt.scatter(df["PCA1"], df["PCA2"], c=labels, cmap="tab10", s=100)
    for i, name in enumerate(df["Company"]):
        plt.text(df["PCA1"][i] + 0.02, df["PCA2"][i], name, fontsize=8)
    plt.title("Competitor Clusters (TF-IDF + PCA)")
    plt.tight_layout()

    plot_path = os.path.join(out_dir, "competitor_clusters.png")
    plt.savefig(plot_path)
    plt.close()

    out_csv = os.path.join(out_dir, "competitor_clusters.csv")
    df.to_csv(out_csv, index=False)

    print(f"[✅] Clustering complete — {k} clusters created.")
    print(f"     → CSV: {out_csv}")
    print(f"     → Plot: {plot_path}")
    return df, plot_path
