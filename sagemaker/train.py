"""
train.py
Simplified script to train or register a time-series anomaly detector.
For demo speed, this script packages a lightweight sklearn model and deploys it as a SageMaker endpoint via a container.
In production, prefer SageMaker JumpStart or a proper training pipeline.
"""
import os
import json
import argparse
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

MODEL_DIR = "model_artifacts"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_dummy_model(seed=42):
    # Create synthetic training data of normal daily costs
    rng = np.random.RandomState(seed)
    # 365 days of values
    X = 100 + rng.randn(365).cumsum() * 0.5
    X = X.reshape(-1, 1)
    model = IsolationForest(contamination=0.01, random_state=seed)
    model.fit(X)
    joblib.dump(model, os.path.join(MODEL_DIR, "anomaly_model.joblib"))
    print("Model saved to", MODEL_DIR)

def score_local(model_path, series):
    import joblib
    m = joblib.load(model_path)
    import numpy as np
    X = np.array(series).reshape(-1, 1)
    preds = m.predict(X)  # -1 anomaly, 1 normal
    scores = m.decision_function(X).tolist()
    anomalies = [i for i, p in enumerate(preds) if p == -1]
    return {"anomalies": anomalies, "scores": scores}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--test_series", nargs="+", type=float)
    args = parser.parse_args()
    if args.train:
        train_dummy_model()
    if args.test_series:
        out = score_local(os.path.join(MODEL_DIR, "anomaly_model.joblib"), args.test_series)
        print(json.dumps(out, indent=2))
