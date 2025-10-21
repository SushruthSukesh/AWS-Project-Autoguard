# AutoGuard Cost Anomaly Model Card

**Model name:** autoguard-cost-anom (demo IsolationForest)

**Description:** Lightweight anomaly detector trained locally on synthetic time-series cost values. Used for demo to surface sudden spikes.

**Intended use:** Assist the AutoGuard agent to flag unusual cost patterns for further investigation by LLM reasoning and remediation steps.

**Limitations & precautions:**
- Demo model is not production-grade. Replace with SageMaker JumpStart/time-series model or an LSTM/Prophet/DeepAR model for production.
- Watch for seasonality and region-specific billing patterns.
- False positives possible; agent includes dry-run and approval gates.

**Data:** synthetic training data (demo). For production, use historical Cost Explorer metrics with proper anonymization and retention controls.

**Metrics:** For the demo, we use `IsolationForest` anomaly flags and a decision function as score.
