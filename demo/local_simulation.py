"""
Demo local simulation for AutoGuard full flow (no real AWS calls).
- Mocks cost analyzer inference
- Mocks Bedrock reasoning
- Mocks remediator execution (prints and records as 'executed')
- Mocks Nova Act call
- Writes a Markdown incident summary to demo/incident_summary.md
"""
import json
from datetime import datetime
import random
import os

print("Initializing AutoGuard local simulation...")

# Step 1: Detection (mocked)
print("Loading SageMaker cost analyzer...")
# create a fake metric series
series = [100.0, 105.0, 110.0, 115.0, 600.0]
print("Running inference on sample metrics...")
# simple anomaly detection: last point > mean * 3
mean = sum(series[:-1]) / (len(series) - 1)
anomaly = series[-1] > mean * 3
confidence = round(random.uniform(0.85, 0.98), 2) if anomaly else round(random.uniform(0.0, 0.5), 2)
if anomaly:
    print(f"[AutoGuard] Alert: Sudden {int((series[-1]/mean - 1)*100)}% cost spike detected in EC2 usage.")
    print("[AutoGuard] Reason: Instance type changed from t3.medium -> p3.2xlarge unexpectedly.")

# Step 2: Reasoning (mocked LLM)
print("Generating remediation plan via Bedrock AgentCore (mock)...")
llm_chain_of_thought = (
    "Potential root cause: unapproved scaling event.\n"
    f"Confidence: {int(confidence*100)}%.\n"
    "Next step: Verify IAM role activity and instance launch origin."
)
print("[AutoGuard] Reasoning:\n" + llm_chain_of_thought)

# Step 3: Action (Autonomous Remediation - mocked)
instance_id = "i-0492abcd"
print("Executing safe remediation via mock remediator...")
# simulate approved stop
executed = {
    "action": "stop_instances",
    "instance_id": instance_id,
    "status": "executed",
}
print(f"[AutoGuard] Remediation: Instance {instance_id} stopped.")
print("[AutoGuard] Verification: Billing stabilized, user notified.")

# Nova Act simulation
print("Invoking Nova Act bridge (mock)...")
print("[AutoGuard] Nova Act: Triggered external notification to Slack (mock).")

# Step 4: Reporting
out_dir = os.path.join(os.path.dirname(__file__), "incident_outputs")
os.makedirs(out_dir, exist_ok=True)
summary_path = os.path.join(out_dir, f"incident-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.md")
summary = {
    "title": "AutoGuard Incident Summary",
    "date": datetime.utcnow().isoformat(),
    "detected": "Unauthorized EC2 Scaling",
    "action_taken": "Instance stopped",
    "verification": "Success (cost anomaly resolved)",
    "ai_confidence": int(confidence*100),
    "model_used": "sagemaker-cost-analyzer-v1",
    "incident_details": {
        "series": series,
        "mean": mean,
        "spike_value": series[-1]
    }
}
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("=== AutoGuard Incident Summary ===\n")
    f.write(f"Date: {datetime.utcnow().isoformat()}\n")
    f.write(f"Detected: {summary['detected']}\n")
    f.write(f"Action Taken: {summary['action_taken']}\n")
    f.write(f"Verification: {summary['verification']}\n")
    f.write(f"AI Confidence: {summary['ai_confidence']}%\n")
    f.write(f"Model Used: {summary['model_used']}\n")
    f.write('\n---\n')
    json.dump(summary, f, indent=2)

print(f"Remediation complete. Log stored in {summary_path}")
