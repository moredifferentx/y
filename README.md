🤖 Discord AI Ecosystem

A production-grade, local-first Discord AI platform with human-like behavior, real-time dashboard control, hot-swappable AI engines, persistent memory, plugin extensibility, and zero-restart operations.

This is not a demo.
This is a real system designed for long-running operation, observability, and extensibility.

✨ Core Highlights

🧠 Human-like cognition

Personality, mood, emotion, memory

Relationship-aware and context-aware

🔀 Hybrid AI engine architecture

Local LLM via Ollama (default)

Cloud fallback (OpenAI, Gemini) via API keys

Hot-swap engines without restart

🖥️ Real-time dashboard

Engine switching

Mood & personality control

Memory & plugin visibility

Live monitoring & logs

🧩 Plugin system

Hot-load / unload

Python & JavaScript support

Permission-aware sandboxing

📊 Observability

CPU / RAM / Disk monitoring

AI engine metrics

Health checks

Live logs

🚀 One-command deployment

Local-first

Docker-ready

No manual steps

🧱 Architecture Overview
Discord
   │
   ▼
Discord Bot  ──▶ Cognition (mood, personality, emotion)
   │                 │
   │                 ▼
   │             Memory System
   │
   ▼
AI Engine Router
   ├── Ollama (local, default)
   ├── OpenAI (cloud fallback)
   └── Gemini (cloud fallback)
   │
   ▼
Dashboard Backend (FastAPI + WebSocket)
   │
   ▼
Dashboard Frontend (React + Vite + Tailwind)


Key design principles:

State isolation between engines

No restarts for hot-swap features

Backend is the single source of truth

Dashboard is fully real-time (no polling)

📁 Repository Structure (Simplified)
.
├── backend/        # FastAPI backend + Discord bot
├── frontend/       # React dashboard
├── plugins/        # Hot-loadable plugins
├── migrations/     # SQLite schemas
├── scripts/        # Setup & dev scripts
├── docs/           # Architecture & API docs
├── start.sh        # One-command deployment
├── docker-compose.yml
├── .env.example
└── README.md

🔧 Requirements
System

Python 3.10+

Node.js 18+

SQLite

Discord Bot Token

(Optional) Ollama installed locally

Python

fastapi

uvicorn

discord.py

psutil

openai

google-generativeai

Frontend

React 18

Vite

TailwindCSS

🚀 Quick Start (One Command)
1️⃣ Clone the repository
git clone https://github.com/yourusername/discord-ai-ecosystem.git
cd discord-ai-ecosystem

2️⃣ Configure environment
cp .env.example .env


Fill in at least:

DISCORD_BOT_TOKEN=your_token_here


(Optional) Add cloud API keys:

OPENAI_API_KEY=
GEMINI_API_KEY=

3️⃣ Start everything
./start.sh


That’s it.

Backend starts on http://localhost:8000

Dashboard WebSocket auto-connects

Discord bot comes online

Memory DB is initialized automatically

🖥️ Dashboard

URL: http://localhost:5173 (dev mode)

Real-time WebSocket updates

Controls:

Active AI engine

Cloud engine enable/disable

Mood & personality

Plugins

Logs & monitoring

No polling.
No refresh required.

🔀 AI Engine System
Supported Engines
Engine	Type	Notes
Ollama	Local	Default, zero cloud dependency
OpenAI	Cloud	API-key based
Gemini	Cloud	API-key based
Behavior

Ollama runs by default

Cloud engines act as fallback or manual override

Engine state is isolated

Switching does not restart the bot

🧠 Memory System

Persistent SQLite-based memory:

User memory – preferences, facts

Server memory – culture, rules

Emotional memory – how users make the bot feel

Ephemeral memory – short-term context

Includes:

Importance scoring

Decay

Emotional influence on mood

See: docs/memory.md

🧩 Plugin System

Hot-loadable

Python & JavaScript

Lifecycle hooks

Permission model

Example plugins included.

See: docs/plugins.md

📊 Monitoring & Logs

Available via dashboard and API:

CPU / RAM / Disk usage

AI engine metrics

Health checks

In-memory log buffer

Designed for:

Long-running uptime

Debugging without restarts

Operational confidence

📄 Documentation
File	Description
docs/architecture.md	System design
docs/api.md	REST & WebSocket APIs
docs/memory.md	Memory model
docs/personality.md	Cognition system
docs/plugins.md	Plugin system
docs/security.md	Security notes
docs/troubleshooting.md	Common issues
docs/roadmap.md	Future plans
🔐 Security Notes

Dashboard is unauthenticated by default

Intended for self-hosted / trusted environments

Future plans include:

Dashboard auth

RBAC

Audit logs

Encrypted memory at rest

See: docs/security.md

🧪 Development Mode

Run backend + frontend separately:

./scripts/dev.sh

🐳 Docker (Optional)
docker-compose up


Docker is optional, not required.

🛣️ Roadmap (Short)

Dashboard authentication & RBAC

Plugin SDK tooling

Memory visualization UI

Multi-agent reasoning

Scheduled behaviors

Metrics export (Prometheus)

🧠 Philosophy

This project is built on the belief that:

AI systems should feel alive, be locally sovereign, and remain operator-controlled.

No black boxes.
No forced cloud dependency.
No fragile restarts.

📜 License

MIT License.
Use freely, modify responsibly.