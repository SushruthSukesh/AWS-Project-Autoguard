"""
remediator.py
Safe remediation Lambda entrypoint and helper functions.
This file is used as the Lambda handler in the CDK stack (for demo).
It supports dry-run and execute modes. Execution of destructive actions requires approval tokens.
"""
import os
import json
import boto3
from datetime import datetime

DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"

ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")
dynamodb = boto3.client("dynamodb")

# allowed actions: stop_instances, tag_resources, rightsizing_recommendation (no destructive delete)
ALLOWED_ACTIONS = {"stop_instances", "tag_resources", "rightsizing_recommendation", "notify"}


def execute_action(action: dict) -> dict:
    """
    action: {
        "type": "stop_instances" | "tag_resources" | "notify",
        "resources": {...},
        "meta": {...}
    }
    """
    action_type = action.get("type")
    if action_type not in ALLOWED_ACTIONS:
        return {"status": "failed", "reason": "action not allowed"}

    if DRY_RUN:
        return {"status": "dry_run", "action": action}

    # Execution paths
    if action_type == "stop_instances":
        instance_ids = action['resources'].get("instance_ids", [])
        if not instance_ids:
            return {"status": "failed", "reason": "no instance ids"}
        resp = ec2.stop_instances(InstanceIds=instance_ids)
        return {"status": "executed", "response": resp}

    if action_type == "tag_resources":
        tags = action['meta'].get("tags", [])
        resources = action['resources'].get("resource_ids", [])
        resp = ec2.create_tags(Resources=resources, Tags=tags)
        return {"status": "executed", "response": resp}

    # Other actions are non-destructive and mocked/stubbed
    return {"status": "executed", "note": "non-destructive action completed"}


def lambda_handler(event, context):
    """
    Lambda entrypoint. Expects event with:
    {
      "incident_id": "...",
      "actions": [ { ...action... } ],
      "approved": false
    }
    """
    incident_id = event.get("incident_id", f"inc-{datetime.utcnow().isoformat()}")
    actions = event.get("actions", [])
    approved = event.get("approved", False)

    results = []
    for act in actions:
        # Simple safety check
        if act.get("type") in ("terminate", "delete"):
            results.append({"status": "skipped", "reason": "destructive action blocked"})
            continue

        if (not approved) and act.get("type") in ("stop_instances",):
            # For stop_instances we allow in dry-run only unless approved
            results.append({"status": "requires_approval", "action": act})
            continue

        res = execute_action(act)
        results.append(res)

    # Log to DynamoDB (if available)
    try:
        table_name = os.environ.get("MEMORY_TABLE", "AgentMemory")
        dynamodb.put_item(TableName=table_name, Item={
            "incident_id": {"S": incident_id},
            "timestamp": {"S": datetime.utcnow().isoformat()},
            "results": {"S": json.dumps(results)}
        })
    except Exception as e:
        print("Dynamo write failed:", e)

    return {"incident_id": incident_id, "results": results}
