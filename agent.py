import os
import sys
import time
from typing import Any, Dict

import requests

BASE_URL = "https://machineid.io"
REGISTER_URL = f"{BASE_URL}/api/v1/devices/register"
VALIDATE_URL = f"{BASE_URL}/api/v1/devices/validate"


def get_org_key() -> str:
    org_key = os.getenv("MACHINEID_ORG_KEY")
    if not org_key:
        raise RuntimeError(
            "Missing MACHINEID_ORG_KEY. Set it in your environment or via a .env file.\n"
            "Example:\n"
            "  export MACHINEID_ORG_KEY=org_your_key_here\n"
        )
    return org_key.strip()


def register_device(org_key: str, device_id: str) -> Dict[str, Any]:
    headers = {
        "x-org-key": org_key,
        "Content-Type": "application/json",
    }
    payload = {
        "deviceId": device_id,
    }

    print(f"→ Registering device '{device_id}' via {REGISTER_URL} ...")
    resp = requests.post(REGISTER_URL, headers=headers, json=payload, timeout=10)
    try:
        data = resp.json()
    except Exception:
        print("❌ Could not parse JSON from register response.")
        print("Status code:", resp.status_code)
        print("Body:", resp.text)
        raise

    status = data.get("status")
    handler = data.get("handler")
    print(f"✔ register response: status={status}, handler={handler}")
    return data


def validate_device(org_key: str, device_id: str) -> Dict[str, Any]:
    headers = {
        "x-org-key": org_key,
    }
    params = {
        "deviceId": device_id,
    }

    print(f"→ Validating device '{device_id}' via {VALIDATE_URL} ...")
    resp = requests.get(VALIDATE_URL, headers=headers, params=params, timeout=10)
    try:
        data = resp.json()
    except Exception:
        print("❌ Could not parse JSON from validate response.")
        print("Status code:", resp.status_code)
        print("Body:", resp.text)
        raise

    status = data.get("status")
    handler = data.get("handler")
    allowed = data.get("allowed")
    reason = data.get("reason")
    print(f"✔ validate response: status={status}, handler={handler}, allowed={allowed}, reason={reason}")
    return data


def main() -> None:
    org_key = get_org_key()
    device_id = os.getenv("MACHINEID_DEVICE_ID", "agent-01")

    print("✔ MACHINEID_ORG_KEY loaded:", org_key[:12] + "...")
    print("Using device_id:", device_id)
    print()

    # 1) Register the device
    reg = register_device(org_key, device_id)
    reg_status = reg.get("status")
    plan_tier = reg.get("planTier")
    limit = reg.get("limit")
    devices_used = reg.get("devicesUsed")
    remaining = reg.get("remaining")

    print()
    print("Registration summary:")
    print("  status       :", reg_status)
    if plan_tier is not None:
        print("  planTier     :", plan_tier)
    if limit is not None:
        print("  limit        :", limit)
    if devices_used is not None:
        print("  devicesUsed  :", devices_used)
    if remaining is not None:
        print("  remaining    :", remaining)
    print()

    if reg_status == "limit_reached":
        print("🚫 Plan limit reached on register. Your agents should treat this as 'do not start'.")
        sys.exit(0)

    # 2) Validate once
    print("Waiting 2 seconds before validating...")
    time.sleep(2)

    val = validate_device(org_key, device_id)
    allowed = val.get("allowed")
    reason = val.get("reason")

    print()
    print("Validation summary:")
    print("  allowed :", allowed)
    print("  reason  :", reason)
    print()

    if allowed:
        print("✅ Device is allowed. In a real agent or worker, this is where you would start or continue work.")
    else:
        print("🚫 Device is NOT allowed. In a real agent or worker, you should exit or pause here.")
        # sys.exit(0)  # Uncomment if you want the starter to actually exit on disallowed

    print()
    print("Done. agent.py completed successfully.")


if __name__ == "__main__":
    main()
