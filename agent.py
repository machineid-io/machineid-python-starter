#!/usr/bin/env python3

import os
import sys
import time
from typing import Any, Dict

import requests

BASE_URL = os.getenv("MACHINEID_BASE_URL", "https://machineid.io").rstrip("/")
REGISTER_URL = f"{BASE_URL}/api/v1/devices/register"
VALIDATE_URL = f"{BASE_URL}/api/v1/devices/validate"


def get_org_key() -> str:
    org_key = os.getenv("MACHINEID_ORG_KEY")
    if not org_key:
        raise RuntimeError(
            "Missing MACHINEID_ORG_KEY.\n"
            "Example:\n"
            "  export MACHINEID_ORG_KEY=org_your_key_here\n"
        )
    return org_key.strip()


def default_device_id() -> str:
    """
    Minimal, deterministic default for demos and starters.
    No local machine info.
    Override with MACHINEID_DEVICE_ID if needed.
    """
    return "python-starter:01"



def post_json(
    url: str,
    headers: Dict[str, str],
    payload: Dict[str, Any],
    timeout_s: int = 10,
) -> Dict[str, Any]:
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout_s)
    try:
        data = resp.json()
    except Exception:
        print("❌ Could not parse JSON response.")
        print("Status code:", resp.status_code)
        print("Body:", resp.text)
        raise

    if resp.status_code >= 400:
        if isinstance(data, dict) and data.get("error"):
            return {
                "status": "error",
                "error": data.get("error"),
                "http": resp.status_code,
            }
        return {
            "status": "error",
            "error": f"HTTP {resp.status_code}",
            "http": resp.status_code,
            "body": data,
        }

    return data


def register_device(org_key: str, device_id: str) -> Dict[str, Any]:
    headers = {"x-org-key": org_key, "Content-Type": "application/json"}
    payload = {"deviceId": device_id}

    print(f"→ Registering device '{device_id}' via {REGISTER_URL} ...")
    data = post_json(REGISTER_URL, headers, payload)

    print(f"✔ register response: status={data.get('status')} handler={data.get('handler')}")
    return data


def validate_device(org_key: str, device_id: str) -> Dict[str, Any]:
    headers = {"x-org-key": org_key, "Content-Type": "application/json"}
    payload = {"deviceId": device_id}

    print(f"→ Validating device '{device_id}' via {VALIDATE_URL} (POST canonical) ...")
    data = post_json(VALIDATE_URL, headers, payload)

    print(
        f"✔ validate decision: "
        f"allowed={data.get('allowed')} "
        f"code={data.get('code')} "
        f"request_id={data.get('request_id')}"
    )
    return data


def main() -> None:
    org_key = get_org_key()
    device_id = (os.getenv("MACHINEID_DEVICE_ID") or "").strip() or default_device_id()

    print("✔ MACHINEID_ORG_KEY loaded:", org_key[:12] + "...")
    print("Using base_url:", BASE_URL)
    print("Using device_id:", device_id)
    print()

    # 1) Register (idempotent)
    reg = register_device(org_key, device_id)
    reg_status = reg.get("status")

    print()
    print("Registration summary:")
    print("  status      :", reg_status)
    if reg.get("planTier") is not None:
        print("  planTier    :", reg.get("planTier"))
    if reg.get("limit") is not None:
        print("  limit       :", reg.get("limit"))
    if reg.get("devicesUsed") is not None:
        print("  devicesUsed :", reg.get("devicesUsed"))
    print()

    if reg_status not in ("ok", "exists"):
        print("🚫 Register did not succeed. Exiting.")
        sys.exit(1)

    # 2) Validate (hard gate)
    time.sleep(1)
    val = validate_device(org_key, device_id)

    allowed = bool(val.get("allowed", False))
    code = val.get("code")
    request_id = val.get("request_id")

    print()
    print("Validation summary:")
    print("  allowed     :", allowed)
    print("  code        :", code)
    print("  request_id  :", request_id)
    print()

    if not allowed:
        print("🚫 Execution denied (hard gate). Exiting immediately.")
        sys.exit(0)

    print("✅ Execution allowed. Start/continue work here.")
    print("Done. agent.py completed successfully.")


if __name__ == "__main__":
    main()
