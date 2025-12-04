# CrewAI + MachineID.io Template

Run a CrewAI agent (or any Python automation) with hard device limits and safe validation checks — no database, no auth system, no infrastructure required.

MachineID.io gives every agent a unique device identity and enforces your plan’s device cap (3 free, higher limits on paid plans).

## 0. Get your free org key (recommended)

1. Visit https://machineid.io
2. Click "Generate free org key"
3. Copy the key (looks like org_...)
4. Set it in your shell:

export MACHINEID_ORG_KEY=org_your_key_here

Or put it in a .env file:

MACHINEID_ORG_KEY=org_your_key_here

This key is sent in the x-org-key header for all requests.

## Advanced: create an org from your backend or agent

Agents or backends can create a free org using:

curl -s https://machineid.io/api/v1/org/create \
  -H "Content-Type: application/json" \
  -d '{}' | jq

Copy the orgApiKey from the response and set:

export MACHINEID_ORG_KEY=org_...from_response...

## Free tier

This template runs on the free plan (3 devices).

If you exceed the limit, MachineID.io returns:

status = limit_reached

Upgrade to unlock 25, 250, or 1000 devices using your existing checkout flow (via dashboard or your backend). Agents can follow the same pattern programmatically.

## Quick start (3 steps)

pip install -r requirements.txt

export MACHINEID_ORG_KEY=org_your_key_here

python agent.py

The script will:
1. Register device agent-01
2. Validate it
3. Show allowed / denied status

## How it works

- Startup → calls /devices/register
- Each loop → calls /devices/validate
- When limit is reached → allowed = false or status = limit_reached

## Files in this repo

- agent.py – working MachineID.io example
- requirements.txt – Python dependencies
- LICENSE – MIT license

## Links

Dashboard → https://machineid.io/dashboard

Documentation → https://machineid.io/docs

MIT licensed · Built by MachineID.io
