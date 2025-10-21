import streamlit as st
import json
from datetime import datetime
import random
import os

st.set_page_config(page_title="AutoGuard Local Demo", layout="centered")
st.title("AutoGuard — Local Simulation Demo")

st.markdown("This app runs a local simulation of the AutoGuard flow (no real AWS calls).")

if st.button("Run Simulation"):
    st.write("Initializing AutoGuard local simulation...")
    series = [100.0, 105.0, 110.0, 115.0, 600.0]
    st.write("Running inference on sample metrics...")
    mean = sum(series[:-1]) / (len(series) - 1)
    anomaly = series[-1] > mean * 3
    confidence = round(random.uniform(0.85, 0.98), 2) if anomaly else round(random.uniform(0.0, 0.5), 2)
    if anomaly:
        st.error(f"[AutoGuard] Alert: Sudden {int((series[-1]/mean - 1)*100)}% cost spike detected in EC2 usage.")
        st.info("[AutoGuard] Reason: Instance type changed from t3.medium -> p3.2xlarge unexpectedly.")

    st.write("Generating remediation plan via Bedrock AgentCore (mock)...")
    llm_chain_of_thought = (
        "Potential root cause: unapproved scaling event.\n"
        f"Confidence: {int(confidence*100)}%.\n"
        "Next step: Verify IAM role activity and instance launch origin."
    )
    st.write("[AutoGuard] Reasoning:")
    st.code(llm_chain_of_thought)

    instance_id = "i-0492abcd"
    st.write("Executing safe remediation via mock remediator...")
    st.success(f"[AutoGuard] Remediation: Instance {instance_id} stopped.")
    st.write("[AutoGuard] Verification: Billing stabilized, user notified.")

    st.write("Invoking Nova Act bridge (mock)...")
    st.write("[AutoGuard] Nova Act: Triggered external notification to Slack (mock).")

    out_dir = os.path.join(os.path.dirname(__file__), "demo", "incident_outputs")
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

    st.success(f"Remediation complete. Log stored in {summary_path}")
    with open(summary_path, 'rb') as f:
        st.download_button('Download Incident Summary', f, file_name=os.path.basename(summary_path))
else:
    st.write("Press 'Run Simulation' to start the local demo.")
