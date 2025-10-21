"""
nova_act_bridge.py
A thin adapter to invoke Nova Act flows (browser automation) via a hypothetical SDK or HTTP API.
This file is a stub: fill in with Nova Act SDK details or REST calls depending on preview availability.
"""

import os
import json
import time
import requests

NOVA_ACT_BASE = os.environ.get("NOVA_ACT_BASE", "https://nova-act.example")  # placeholder
NOVA_ACT_API_KEY = os.environ.get("NOVA_ACT_API_KEY", None)


def run_flow(flow_spec: dict) -> dict:
    """
    flow_spec: { "flow_id": "...", "inputs": {...} }
    Returns run result (status, log, screenshots_url)
    """
    if not NOVA_ACT_API_KEY:
        return {"status": "not_configured", "reason": "NOVA_ACT_API_KEY not set"}

    url = f"{NOVA_ACT_BASE}/runs"
    headers = {"Authorization": f"Bearer {NOVA_ACT_API_KEY}", "Content-Type": "application/json"}
    payload = {"flow_spec": flow_spec}
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    if resp.status_code != 200:
        return {"status": "error", "code": resp.status_code, "text": resp.text}
    return resp.json()


if __name__ == "__main__":
    # demo stub; in production, provide a real flow_spec and API key
    print(run_flow({"flow_id": "demo-rightsize", "inputs": {"instance_id": "i-0123456789"}}))
