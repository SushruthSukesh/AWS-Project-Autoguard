"""
Very simple e2e simulation:
- Ensures the remediator Lambda can be invoked with a simulated incident
- Validates DynamoDB write (if table exists)
"""
import boto3
import json
import os
from time import sleep

lambda_client = boto3.client("lambda")
dynamodb = boto3.client("dynamodb")

LAMBDA_NAME = os.environ.get("REMEDIATOR_LAMBDA", "RemediatorFunction")
MEMORY_TABLE = os.environ.get("MEMORY_TABLE", "AgentMemory")

payload = {
    "incident_id": "e2e-demo-001",
    "actions": [
        {"type": "notify", "meta": {"message": "e2e test"}}
    ],
    "approved": False
}

resp = lambda_client.invoke(FunctionName=LAMBDA_NAME, InvocationType="RequestResponse", Payload=json.dumps(payload))
print("Lambda returned:", resp['StatusCode'])
print(resp['Payload'].read().decode("utf-8"))

# Optionally check DynamoDB for entry
try:
    sleep(1)
    resp = dynamodb.get_item(TableName=MEMORY_TABLE, Key={"incident_id": {"S": payload["incident_id"]}})
    print("DynamoDB item:", resp.get("Item"))
except Exception as e:
    print("DynamoDB check skipped or failed:", e)
