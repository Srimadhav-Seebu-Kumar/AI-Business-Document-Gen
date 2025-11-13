import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

def simulate_revenue_monthly(months=12, start=1, growth=0.15, noise=0.05):
    # synthetic historic 12 months, then predict next 12
    hist = np.array([start * ((1+growth)**i) for i in range(months)]) * (1 + np.random.randn(months)*noise)
    return pd.DataFrame({"month": np.arange(1, months+1), "revenue": hist})

def fit_and_project(df, horizon=12, out_dir="data/generated"):
    X = df[["month"]].values
    y = df["revenue"].values
    model = LinearRegression().fit(X, y)
    last = df["month"].max()
    future_months = np.arange(last+1, last+horizon+1)
    y_pred = model.predict(future_months.reshape(-1,1))
    proj = pd.DataFrame({"month": future_months, "predicted_revenue": y_pred})

    # Runway (toy): assume fixed monthly burn
    monthly_burn = y.mean()*0.6
    # simple plot
    os.makedirs(out_dir, exist_ok=True)
    plt.figure()
    plt.plot(df["month"], df["revenue"], label="historic")
    plt.plot(proj["month"], proj["predicted_revenue"], label="projected")
    plt.xlabel("Month"); plt.ylabel("Revenue"); plt.legend(); plt.tight_layout()
    plot_path = os.path.join(out_dir, "finance_projection.png")
    plt.savefig(plot_path); plt.close()
    return proj, monthly_burn, plot_path
