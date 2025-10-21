# AutoGuard — README

## Overview
AutoGuard is an autonomous agent that detects cost anomalies and low-severity security issues in an AWS account, explains causes, and performs safe remediations or requests approval.

## Quickstart (local/dev)
1. Install dependencies:
   - Python 3.11
   - pip install -r requirements.txt (boto3, aws-cdk-lib, scikit-learn, joblib, requests)
2. Deploy infra
   ```bash
   cd infra
   cdk synth
   cdk deploy


Train demo model

python ../sagemaker/train.py --train


Start agent (AgentCore runtime simulated by starting a small local process that polls events) — see agentcore/README (TODO).

Trigger demo

python ../demo/trigger_spike.py

Notes

Replace placeholder Bedrock model IDs and Nova Act endpoints with actual values available in your account/region.

Use AWS Secrets Manager to store credentials and API keys.


---

## Architecture Diagram (required)

The architecture diagram is included in this repository as `docs/architecture_diagram.svg` (and `docs/architecture_diagram.png` placeholder).

Key components and interactions:
- Observability / Data Sources: CloudWatch metrics, Cost Explorer, GuardDuty — feed events/metrics to the Agent.
- Bedrock AgentCore: LLM-based planner and tool invoker. Receives events, calls the SageMaker endpoint, reasons about remediation actions, and coordinates tools.
- SageMaker Endpoint: Hosts the time-series anomaly detector (IsolationForest demo). Returns anomaly indices and scores.
- Lambda Remediator: Performs safe AWS operations (stop, tag) in dry-run mode by default; writes results to DynamoDB and S3.
- Nova Act Bridge: Optional browser automation / external flows for vendor portal tasks and notifications.
- S3 & DynamoDB: Artifact and incident storage (audit logs, model evidence, incident records).
- Streamlit Demo UI: Simple app to run local simulations and download incident summaries.

See `docs/architecture_diagram.svg` for a visual representation of these interactions.
