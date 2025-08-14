import os, json
import pandas as pd
from pathlib import Path
from pymatgen.core.structure import Structure

RAW = Path("data/raw")
PROC = Path("data/processed")
CIF_DIR = PROC / "cif"
CIF_DIR.mkdir(parents=True, exist_ok=True)

# Expect a CSV with columns: structure (as dict/str), gap pbe (float), and maybe an id column
IN_CSV = RAW / "matbench_mp_gap.csv"
OUT_CSV = PROC / "id_prop.csv"


def to_structure(s):
    # Already a dict from somewhere else
    if isinstance(s, dict):
        return Structure.from_dict(s)

    # Expect a string at this point
    if not isinstance(s, str):
        raise ValueError(f"structure is not a string (got {type(s)})")

    t = s.strip()
    if t == "" or t.lower() in {"nan", "none", "null"}:
        raise ValueError("structure is empty/missing")

    # Try to decode once or twice (handles double-encoded JSON)
    for _ in range(2):
        obj = json.loads(t)
        if isinstance(obj, str):
            # was a JSON string of another JSON string → decode again
            t = obj
            continue
        if not isinstance(obj, dict):
            raise ValueError(f"decoded structure is {type(obj)}, expected dict")
        return Structure.from_dict(obj)

    raise ValueError("could not parse structure JSON")

def main():
    df = pd.read_csv(IN_CSV, dtype={"structure": str}, keep_default_na=False)
    #df = pd.read_csv(IN_CSV)
    # Create an ID if none exists
    if "id" not in df.columns:
        df["id"] = [f"matbench_{i:06d}" for i in range(len(df))]
    # Rename/standardize target column
    if "gap pbe" in df.columns:
        df["target"] = df["gap pbe"]
    elif "gap_pbe" in df.columns:
        df["target"] = df["gap_pbe"]
    else:
        raise ValueError("Could not find a gap pbe column.")

    ids, targets = [], []
    bad = 0
    for row in df.itertuples(index=False):
        sid = getattr(row, "id", None)
        raw_s = getattr(row, "structure")
        try:
            structure = to_structure(raw_s)
        except Exception as e:
            bad += 1
            print(f"[warn] skipping id={sid}: {e}  (starts with {repr(str(raw_s)[:60])})")
            continue
    
        cif_path = CIF_DIR / f"{sid}.cif"
        structure.to(filename=str(cif_path))
        ids.append(sid)
        targets.append(float(getattr(row, "target")))
    
    print(f"Skipped {bad} bad rows.")


    pd.DataFrame({"id": ids, "target": targets}).to_csv(OUT_CSV, index=False)
    print(f"Wrote {len(ids)} CIFs to {CIF_DIR} and labels to {OUT_CSV}")

if __name__ == "__main__":
    main()

