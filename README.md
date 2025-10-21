# AutoGuard — Autonomous Cost & Security Agent (Demo)

This repository contains a demo implementation of AutoGuard — an autonomous agent prototype that:
- Detects cost anomalies (SageMaker)
- Uses an LLM (Amazon Bedrock) for planning and explanations (agent_config.yaml)
- Executes safe remediations via Lambda (dry-run by default)
- Optionally automates browser-only tasks with Nova Act

## Contents
See the repo tree. Key entry points:
- `infra/` — CDK deployment for basic infra (S3, DynamoDB, Lambda)
- `agentcore/` — agent config and tools
- `sagemaker/` — demo training script and model card
- `demo/` — demo trigger and scripts
- `tests/` — unit and e2e tests

## Next steps
- Replace placeholder Bedrock model IDs with real models in your region.
- Add an AgentCore runtime (this demo assumes you provide or run AgentCore runtime that reads `agent_config.yaml` and wires the tools).
- Harden IAM policies, secrets management, and monitoring.

---

## License

This project is provided under the MIT License. See the `LICENSE` file for details.


