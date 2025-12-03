# CrewAI + MachineID.io Template

Run a CrewAI fleet with hard registration caps and per-agent validation — no custom database or auth required.

## Why use this
- Automatically block new agents when you hit your plan limit (3 / 25 / 250 / 1000)
- Prevent runaway OpenAI bills
- Zero extra dependencies

## Quick start (3 steps)

pip install crewai machineid
export MACHINEID_ORG_KEY=mid_********************************
python crew.py

That’s it — the first agent registers itself, every subsequent agent validates against MachineID.io.

## How it works
1. On startup → agent calls /devices/register (idempotent)
2. Every loop → agent calls /devices/validate
3. When limit is reached → registration fails → agent exits gracefully

## Files in this repo
- crew.py – complete working example
- .env.example – put your org key here

## Links
- Dashboard & upgrade → https://machineid.io/dashboard
- Full docs → https://machineid.io/docs

MIT licensed · Built by MachineID.io
