# MachineID.io Python Starter Template
### Add device limits to Python agents with one small register/validate block.

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
    - `ok` / `exists` / `restored`  
    - `limit_reached`  
    - `allowed` / `not_allowed`
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

### 1. Clone this repo or click **“Use this template.”**

```bash
git clone https://github.com/machineid-io/machineid-python-starter.git
cd machineid-python-starter
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Get a free org key (supports 3 devices)

Visit https://machineid.io  
Click **“Generate free org key”**  
Copy the key (it begins with `org_`)

---

### 4. Export your org key

```bash
export MACHINEID_ORG_KEY=org_your_org_key_here
```

**One-liner (run immediately):**

```bash
MACHINEID_ORG_KEY=org_xxx python agent.py
```

---

### 5. Run the starter

```bash
python agent.py
```

You'll see a register call, a validate call, and a summary showing whether this device is allowed.

---

## How the script works

1. Reads `MACHINEID_ORG_KEY` from the environment  
2. Uses a default `deviceId` of `python-starter:01`
   -  You may override this by setting MACHINEID_DEVICE_ID.
3. Calls `/api/v1/devices/register`:
   - ok → new device created  
   - exists → device already registered  
   - error → registration failed (including revoked devices or plan limits)
 
4. Calls `/api/v1/devices/validate`:
   - allowed: true  → execution may continue  
   - allowed: false → execution must stop immediately  
     (decision is identified by `code` and `request_id`)


This simple cycle prevents uncontrolled scaling and mirrors the behavior of real production fleets.

---

## Using this in your own agents

To integrate MachineID.io:

- Call **register** when your agent starts  
- Call **validate**:
  - Before each major task, or  
  - On intervals for long-running loops  
- Continue only when `allowed == true`  

This prevents accidental over-scaling and uncontrolled agent spawning.

**Drop the same register/validate block into any Python worker, task runner, or background script.**  
This is all you need to enforce simple device limits across your entire system.

---

## Files in this repo

- `agent.py` — Universal Python starter (register + validate)  
- `requirements.txt` — Minimal dependency (`requests`)  
- `LICENSE` — MIT licensed  

Optional `.env` pattern:

```bash
MACHINEID_ORG_KEY=org_your_org_key_here
```

---

## Links

Dashboard → https://machineid.io/dashboard  
Generate free org key → https://machineid.io  
Docs → https://machineid.io/docs  
API → https://machineid.io/api  

---

## Other templates

→ LangChain:     https://github.com/machineid-io/langchain-machineid-template  
→ CrewAI:        https://github.com/machineid-io/crewai-machineid-template  
→ OpenAI Swarm:  https://github.com/machineid-io/swarm-machineid-template  

---

## How plans work (quick overview)

- Plans are per **org**, each with its own `orgApiKey`  
- Device limits apply to unique `deviceId` values registered through `/devices/register`  
- When you upgrade or change plans in Stripe, limits update immediately — **your agents do not need new code**  

MIT licensed · Built by MachineID.io
