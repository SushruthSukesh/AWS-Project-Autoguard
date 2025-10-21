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
