"""
cost_analyzer.py
Simple wrapper that posts a metric series to a SageMaker endpoint for anomaly scoring.
This is a lightweight client; in production, secure credentials and error handling are required.
"""
import os
import json
import boto3
from typing import Dict, Any

_SMR_CLIENT = None
ENDPOINT_NAME = os.environ.get("COST_ANOM_ENDPOINT", "autoguard-cost-anom-endpoint")


def _get_smr_client():
    """Lazily create the sagemaker-runtime client. Returns None if region not configured."""
    global _SMR_CLIENT
    if _SMR_CLIENT is not None:
        return _SMR_CLIENT
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not region:
        # Avoid raising at import time; caller should handle None client (e.g., in tests)
        return None
    _SMR_CLIENT = boto3.client("sagemaker-runtime", region_name=region)
    return _SMR_CLIENT


def score_cost_anomaly(metric_series: Dict[str, Any]) -> Dict[str, Any]:
    """
    metric_series: {
        "timestamps": [...],
        "values": [...],
        "granularity": "hourly" | "daily"
    }
    """
    payload = {"input": metric_series}
    client = _get_smr_client()
    if client is None:
        raise RuntimeError("No AWS region configured for SageMaker client. Set AWS_REGION or AWS_DEFAULT_REGION.")
    resp = client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=json.dumps(payload)
    )
    body = resp['Body'].read().decode("utf-8")
    result = json.loads(body)
    return result


if __name__ == "__main__":
    # quick local test (requires AWS credentials and an endpoint)
    example = {"timestamps": ["2025-10-01", "2025-10-02", "2025-10-03"], "values": [100, 120, 600], "granularity": "daily"}
    print(score_cost_anomaly(example))
