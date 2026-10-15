\"\"\"Train a detector from JSONL events (one event JSON object per line).

This starter script prints guidance because the online demo currently uses a
synthetic baseline. For a production implementation, curate labeled/verified
normal events, build a consistent feature matrix, evaluate on held-out data,
and version the resulting model. Do not train on unreviewed alerts as ground truth.
\"\"\"
import argparse, json
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.ensemble import IsolationForest
from app.detector import event_features

def main():
    p = argparse.ArgumentParser()
    p.add_argument("jsonl", help="Path to reviewed baseline JSONL")
    p.add_argument("--out", default="data/isolation_forest.joblib")
    args = p.parse_args()
    rows = [json.loads(x) for x in Path(args.jsonl).read_text().splitlines() if x.strip()]
    counts = Counter(r.get("src_ip", "") for r in rows)
    X = np.asarray([event_features(r, counts) for r in rows])
    model = IsolationForest(n_estimators=200, contamination="auto", random_state=42).fit(X)
    import joblib
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.out)
    print(f"Saved model to {args.out}. Evaluate false positives before deployment.")

if __name__ == "__main__":
    main()
