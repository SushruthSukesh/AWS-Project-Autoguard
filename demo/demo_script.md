# AutoGuard Demo Script (~3 minutes)

## 0:00 - 0:20 — Intro & problem statement
- Slide: "AutoGuard — Autonomous Cloud Cost & Security Remediation Agent"
- Show architecture diagram.

## 0:20 - 0:50 — Trigger synthetic incident
- Run: `python demo/trigger_spike.py` (creates a simulated cost spike / EventBridge event).
- Show Cost Explorer or CloudWatch synthetic metric spike.

## 0:50 - 1:40 — Agent detects & investigates
- Show Lambda logs / AgentCore logs:
  - SageMaker scoring returns anomaly indices.
  - Bedrock Planner returns chain-of-thought (short) for root cause: e.g., "untagged dev instances in us-east-1, autoscale misconfig".
- Show evidence stored in S3 (metric snapshot) and DynamoDB (incident record).

## 1:40 - 2:20 — Agent proposes remediation + executes safe ops
- Agent proposes a rightsizing stop action. Because default mode is `dry_run`, it shows a recommended `stop_instances` action requiring approval.
- Demonstrate approval flow:
  - Click approve button (or run CLI `python demo/approve_and_execute.py --incident <id>`)
  - Show remediator Lambda executing and returning success
- Show CloudWatch/EC2 console showing instance state change.

## 2:20 - 2:50 — Optional Nova Act run
- Show Nova Act executed to log into vendor portal (demo stub) and archive an account.
- Show logs/screenshots.

## 2:50 - 3:00 — Wrap up
- Show metrics: $ saved estimate, incident log, link to repo.
