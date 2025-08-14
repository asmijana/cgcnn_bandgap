import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import matplotlib.pyplot as plt

CGCNN_DIR = Path("external/cgcnn")
pred_path = CGCNN_DIR / "test_results.csv"  # CGCNN writes predictions by default
if not pred_path.exists():
    raise FileNotFoundError("test_results.csv not found. Did training finish?")

df = pd.read_csv(pred_path, header=None, names=["id", "y_true", "y_pred"])
mae = mean_absolute_error(df["y_true"], df["y_pred"])
rmse = root_mean_squared_error(df["y_true"], df["y_pred"])

metrics = {"test/MAE": mae, "test/RMSE": rmse}
(CGCNN_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))

# Parity plot
plt.figure()
plt.scatter(df["y_true"], df["y_pred"], s=12, alpha=0.6)
mn = min(df["y_true"].min(), df["y_pred"].min())
mx = max(df["y_true"].max(), df["y_pred"].max())
plt.plot([mn, mx], [mn, mx], linewidth=2)
plt.xlabel("True band gap (eV)")
plt.ylabel("Predicted band gap (eV)")
plt.title("CGCNN Parity (Test)")
figpath = CGCNN_DIR / "parity_plot.png"
plt.savefig(figpath, dpi=200, bbox_inches="tight")
print(json.dumps(metrics, indent=2))
print(f"Saved parity plot to {figpath}")

