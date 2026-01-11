# API Reference — Discord AI Ecosystem

This document describes the **public and internal APIs** exposed by the Discord AI Ecosystem backend.

The backend is built with **FastAPI** and exposes:
- REST APIs for control and configuration
- WebSocket APIs for real-time dashboard synchronization

---

## Base URLs

### REST API
http://localhost:8000/api/dashboard

shell
Copy code

### WebSocket
ws://localhost:8000/ws/dashboard

yaml
Copy code

---

## Authentication

> ⚠️ Currently, dashboard APIs are **unauthenticated** by default.

Future versions may enforce:
- Admin tokens
- Role-based access
- 2FA

See `docs/security.md`.

---

# REST API

## AI Engine Control

### Get available engines
**GET**
/ai/engines

pgsql
Copy code

**Response**
```json
{
  "engines": ["ollama", "openai", "gemini"],
  "active": "ollama",
  "fallback": "openai"
}
Set active engine
POST

bash
Copy code
/ai/engine/active?engine_id=ollama
Switches the active AI engine at runtime.

No restart required

State-isolated

Set fallback engine
POST

bash
Copy code
/ai/engine/fallback?engine_id=openai
Used when the active engine fails.

Cloud Engine Control
Cloud engine status
GET

bash
Copy code
/cloud/status
Response

json
Copy code
{
  "openai": true,
  "gemini": false
}
Enable / Disable cloud engine
POST

bash
Copy code
/cloud/toggle/{engine}?enabled=true
Supported engines:

openai

gemini

This reloads .env and re-registers providers dynamically.

Cognition System
Get cognition state
GET

bash
Copy code
/cognition
Response

json
Copy code
{
  "personality": { "friendly": 0.7, "logical": 0.5 },
  "mood": { "mood": "neutral", "intensity": 0.4 }
}
Set mood
POST

bash
Copy code
/cognition/mood?mood=happy
Update personality
POST

bash
Copy code
/cognition/personality
Body

json
Copy code
{
  "friendly": 0.8,
  "chaotic": 0.2
}
Monitoring
Hardware stats
GET

bash
Copy code
/monitoring/hardware
Response

json
Copy code
{
  "cpu_percent": 23.1,
  "memory": { "total": 16777216, "used": 7340032, "percent": 43.7 },
  "disk": { "total": 512000000000, "used": 230000000000, "percent": 44.9 }
}
AI engine metrics
GET

bash
Copy code
/monitoring/metrics
Response

json
Copy code
{
  "ollama": { "latency_ms": 320, "tokens_per_sec": 42 },
  "openai": { "latency_ms": 810 }
}
Health check
GET

bash
Copy code
/monitoring/health
Response

json
Copy code
{
  "status": "ok",
  "engines": {
    "ollama": true,
    "openai": true,
    "gemini": false
  }
}
Logs
GET

bash
Copy code
/monitoring/logs
Returns the latest in-memory log buffer.

Plugins
List plugins
GET

bash
Copy code
/plugins
Response

json
Copy code
["example_plugin"]
Enable plugin
POST

bash
Copy code
/plugins/enable/{plugin_name}
Disable plugin
POST

bash
Copy code
/plugins/disable/{plugin_name}
WebSocket API
Dashboard WebSocket
Connection
bash
Copy code
ws://localhost:8000/ws/dashboard
This WebSocket provides real-time, push-based synchronization between backend and dashboard.

Initial State Message
Sent immediately after connection.

json
Copy code
{
  "type": "init",
  "state": {
    "active_engine": "ollama",
    "engines": ["ollama", "openai"],
    "cloud": { "openai": true, "gemini": false },
    "plugins": ["example_plugin"],
    "personality": { "friendly": 0.7 },
    "mood": { "mood": "neutral" },
    "hardware": { "...": "..." },
    "metrics": { "...": "..." },
    "logs": []
  }
}
Engine Switch Event
json
Copy code
{
  "type": "engine.switch",
  "engine": "openai"
}
Mood Update Event
json
Copy code
{
  "type": "mood.update",
  "mood": "happy"
}
Plugin Events
Plugin Loaded
json
Copy code
{
  "type": "plugin.loaded",
  "plugin": "example_plugin"
}
Plugin Unloaded
json
Copy code
{
  "type": "plugin.unloaded",
  "plugin": "example_plugin"
}
Monitoring Update
Sent periodically (~2s).

json
Copy code
{
  "type": "monitoring.update",
  "hardware": { "...": "..." },
  "metrics": { "...": "..." },
  "logs": ["..."]
}
Notes
All state changes are authoritative from the backend

Frontend must treat WS data as source of truth

REST APIs are used for commands

WebSocket is used for state propagation

Related Docs
architecture.md

memory.md

plugins.md

security.md

roadmap.md

yaml
Copy code

---

# ✅ STEP 5 STATUS

| Item | Status |
|---|---|
| REST docs | ✅ Complete |
| WS docs | ✅ Complete |
| Monitoring docs | ✅ Complete |
| Plugin docs | ✅ Complete |
| Accurate to code | ✅ |
| No speculation | ✅ |

This **closes the last documentation gap**.

---

## 🏁 FINAL CLEANUP ITEMS LEFT

From the audit, only **two** remain:

1️⃣ **Plugin directory casing fix** (Linux/Docker critical)  
2️⃣ **Cloud engine deprecation cleanup**  

After that → **release-ready**.

Tell me the next number, or say **FINAL ZIP** if you want packaging instructions.