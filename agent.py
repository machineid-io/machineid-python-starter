import os
import sys
import time
import requests

from crewai import Agent as CrewAgent, Task as CrewTask, Crew

BASE_URL = "https://machineid.io/api/v1"


def get_org_key() -> str:
  org_key = os.getenv("MACHINEID_ORG_KEY")
  if not org_key:
    print("❌ MACHINEID_ORG_KEY is not set. Please export it or add it to your .env.")
    sys.exit(1)
  print(f"✔ MACHINEID_ORG_KEY loaded: {org_key[:12]}...")
  return org_key


def register_device(org_key: str, device_id: str) -> dict:
  url = f"{BASE_URL}/devices/register"
  headers = {
    "Content-Type": "application/json",
    "x-org-key": org_key,
  }
  payload = {
    "deviceId": device_id,
  }

  print(f"\n→ Registering device '{device_id}' via {url} ...")

  try:
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    data = resp.json()
  except Exception as e:
    print(f"❌ Error calling devices/register: {e}")
    sys.exit(1)

  status = data.get("status")
  handler = data.get("handler")
  print(f"✔ register response: status={status}, handler={handler}")

  print("\nRegistration summary:")
  print(f"  status       : {data.get('status')}")
  print(f"  planTier     : {data.get('planTier')}")
  print(f"  limit        : {data.get('limit')}")
  print(f"  devicesUsed  : {data.get('devicesUsed')}")
  print(f"  remaining    : {data.get('remaining')}")

  return data


def validate_device(org_key: str, device_id: str) -> dict:
  url = f"{BASE_URL}/devices/validate"
  headers = {
    "Content-Type": "application/json",
    "x-org-key": org_key,
  }
  payload = {
    "deviceId": device_id,
  }

  print("\nWaiting 2 seconds before validating...")
  time.sleep(2)

  print(f"→ Validating device '{device_id}' via {url} ...")

  try:
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    data = resp.json()
  except Exception as e:
    print(f"❌ Error calling devices/validate: {e}")
    sys.exit(1)

  status = data.get("status")
  handler = data.get("handler")
  allowed = data.get("allowed")
  reason = data.get("reason")

  print(f"✔ validate response: status={status}, handler={handler}, allowed={allowed}, reason={reason}")

  print("\nValidation summary:")
  print(f"  allowed : {allowed}")
  print(f"  reason  : {reason}")

  return data


def run_crewai_example():
  """
  Minimal CrewAI demo:
  - Uses your OPENAI_API_KEY (or other provider configured in CrewAI)
  - Runs a single, simple task
  """
  print("\n🚀 Device is allowed. Starting simple CrewAI task...")

  # A single agent that describes MachineID.io in one sentence
  agent = CrewAgent(
    role="AI Fleet Engineer",
    goal="Explain what MachineID.io does in one clear, short sentence.",
    backstory=(
      "You help developers understand infrastructure tools that keep AI agents under control. "
      "You are concise, direct, and avoid marketing fluff."
    ),
    verbose=True,
  )

  task = CrewTask(
    description="In one short sentence, explain what MachineID.io does for AI agents and device fleets.",
    agent=agent,
    expected_output="A single, clear sentence describing MachineID.io."
  )

  crew = Crew(
    agents=[agent],
    tasks=[task],
  )

  try:
    result = crew.kickoff()
  except Exception as e:
    print(f"❌ CrewAI run failed (check OPENAI_API_KEY or provider config): {e}")
    return

  print("\n✅ CrewAI result:")
  print(result)


def main():
  org_key = get_org_key()
  device_id = "agent-01"
  print(f"Using device_id: {device_id}")

  # 1) Register the device
  reg = register_device(org_key, device_id)
  reg_status = reg.get("status")

  if reg_status in ("ok", "exists", "restored"):
    pass
  elif reg_status == "limit_reached":
    print("\n🚫 Device limit reached for this org. Upgrade your plan to register more devices.")
    sys.exit(0)
  else:
    print("\n🚫 Registration failed with unexpected status. Not continuing.")
    sys.exit(1)

  # 2) Validate the device
  val = validate_device(org_key, device_id)
  allowed = val.get("allowed", False)

  if not allowed:
    print("\n🚫 Device is NOT allowed. In a real agent, you should exit or pause here.")
    sys.exit(0)

  print("\n✅ Device is allowed. In a real agent, this is where work would start.")
  # 3) Run a tiny CrewAI example so this template is a true CrewAI + MachineID demo
  run_crewai_example()

  print("\nDone. agent.py completed successfully.")


if __name__ == "__main__":
  main()
