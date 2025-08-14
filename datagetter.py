from matminer.datasets import load_dataset
import pandas as pd
from pathlib import Path
import json

RAW = Path("data/raw")
OUT_CSV = RAW / "matbench_mp_gap.csv"
RAW.mkdir(parents=True, exist_ok=True)

df = load_dataset("matbench_mp_gap")
df["structure"] = df["structure"].apply(lambda s: json.dumps(s.as_dict()))
df.to_csv(OUT_CSV, index=False)
