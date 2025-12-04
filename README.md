# MachineID.io Python Starter Template

A minimal, universal starting point for adding MachineID.io device registration and validation to any Python-based agent or script.

Use this starter to prevent runaway fleets, enforce hard device limits, and ensure every agent checks in before doing work.  
The free org key supports up to **3 devices**, with higher limits available on paid plans.

---

## What this repo gives you

- A tiny Python script (`agent.py`) that:
  - Reads `MACHINEID_ORG_KEY` from the environment
  - Calls `/api/v1/devices/register` with `x-org-key` and a `deviceId`
  - Calls `/api/v1/devices/validate` before running
  - Prints clear status:
    - ok / exists / restored  
    - limit_reached (free tier = 3 devices)  
    - allowed / not allowed
- A minimal `requirements.txt` using only `requests`
- A pattern suitable for:
  - CrewAI agents
  - OpenAI Swarm workers
  - LangChain / LCEL chains
  - Custom agent loops
  - Cron jobs or background workers

This is the base template all other MachineID.io examples build on.

---

## Quick start

1. Clone this repo or click **“Use this template.”**

2. Install dependencies:

   pip install -r requirements.txt

3. Get a free org key (supports 3 devices):  
   - Visit https://machineid.io  
   - Click **“Generate free org key”**  
   - Copy the key (it begins with `org_...`)

4. Export your org key:

   export MACHINEID_ORG_KEY=org_your_org_key_here

5. Run the starter:

   python agent.py

You’ll see a register call, a validate call, and a summary of whether this device is allowed.

---

## How the script works

1. Reads `MACHINEID_ORG_KEY` from the environment.  
2. Uses a default `deviceId` of `agent-01`.  
3. Calls `/api/v1/devices/register`:
   - `ok` → new device created  
   - `exists` → device already registered  
   - `restored` → previously revoked device restored  
   - `limit_reached` → free tier cap hit  
4. Calls `/api/v1/devices/validate`:
   - `allowed: true` → agent should run  
   - `allowed: false` → agent should stop or pause  

This is the exact control cycle used by real fleets.

---

## Using this in your own agents

To integrate with MachineID.io:

- Call **register** when the agent starts.  
- Call **validate**:
  - Before each major task, or  
  - On a time interval for long-running agents.  
- Only continue when `allowed` is true.  

This prevents accidental over-scaling and uncontrolled agent spawning.

---

## Advanced: create orgs programmatically (optional)

Most humans generate a free org key from the dashboard.

Fully automated backends or meta-agents may instead call:

POST /api/v1/org/create

Example:

curl -s https://machineid.io/api/v1/org/create \
  -H "Content-Type: application/json" \
  -d '{}'

The response includes an `orgApiKey` that works exactly like dashboard-created keys.

---

## Files in this repo

- `agent.py` — Universal Python starter (register + validate)  
- `requirements.txt` — Minimal dependency (`requests`)  
- `LICENSE` — MIT licensed  

Optional `.env` pattern:

MACHINEID_ORG_KEY=org_your_org_key_here

---

## Links

Dashboard → https://machineid.io/dashboard  
Generate free org key → https://machineid.io  
Docs → https://machineid.io/docs  
API → https://machineid.io/api  

---

## How plans work (quick overview)

- Plans are per **org**, each with its own `orgApiKey`.  
- Device limits apply to unique `deviceId` values registered via `/devices/register`.  
- When you upgrade or change plans in Stripe, limits update immediately — **your agents do not need new code**.

MIT licensed · Built by MachineID.io
