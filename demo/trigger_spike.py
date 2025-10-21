"""
Trigger a simulated EventBridge event to emulate a cost spike.
For demo, this posts an invocation to the Remediator Lambda via boto3 invoke (or EventBridge put_events)
"""
import boto3
import json
import os
from datetime import datetime

lambda_client = boto3.client("lambda")
payload = {
    "incident_id": f"demo-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
    "actions": [
        {
            "type": "notify",
            "resources": {},
            "meta": {"message": "Simulated cost spike detected in us-east-1. Suggested rightsizing: stop i-0123456789abcde"}
        }
    ],
    "approved": False
}

LAMBDA_NAME = os.environ.get("REMEDIATOR_LAMBDA", "RemediatorFunction")

resp = lambda_client.invoke(
    FunctionName=LAMBDA_NAME,
    InvocationType="RequestResponse",
    Payload=json.dumps(payload)
)
print("Lambda response:", resp['Payload'].read().decode("utf-8"))
