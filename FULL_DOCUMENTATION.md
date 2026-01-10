# Discord AI Chatbot - Complete Documentation

## Overview

This is a **production-grade Discord AI chatbot** with:
- **Hybrid LLM Architecture**: Local Ollama + Cloud OpenAI fallback
- **Human-Like Behavior**: Mood system, personality, emotional memory
- **Full Dashboard Control**: Real-time WebSocket controls, monitoring, configuration
- **Advanced Features**: Plugin system, image generation, multi-language support, relationship scoring
- **System Monitoring**: Uptime tracking, health checks, logs, restart controls

## Quick Start

### 1. Clone and Setup

```bash
cd /workspaces/y
cp .env.example .env
# Edit .env with your tokens
```

### 2. Run Everything with One Command

```bash
chmod +x start.sh
./start.sh
```

This will:
- Create Python virtual environment
- Install dependencies
- Initialize database
- Start FastAPI backend (port 8000)
- Start Discord bot (async)
- Dashboard available at `http://localhost:8000/static/index.html`

### 3. Get Your Tokens

**Discord Bot Token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Go to Bot tab → Add Bot
4. Copy token and add to `.env` as `DISCORD_BOT_TOKEN`
5. Enable "Message Content Intent" under Privileged Gateway Intents

**OpenAI API Key (optional fallback):**
1. Go to [OpenAI](https://platform.openai.com)
2. Create API key
3. Add to `.env` as `OPENAI_API_KEY`

**Ollama Setup (local LLM):**
1. Install [Ollama](https://ollama.ai)
2. Run: `ollama run llama2`
3. Default endpoint is `http://localhost:11434`

## Architecture

### Core Modules

```
backend/
├── app.py                 # FastAPI main app with all endpoints
├── ai/
│   ├── engine.py         # AIManager (hot-swappable engines)
│   ├── ollama_client.py  # Local LLM client
│   └── cloud_client.py   # Cloud LLM client (OpenAI)
├── bot/
│   └── discord_bot.py    # Enhanced Discord bot (slash commands, reactions)
├── memory.py             # Memory storage with decay
├── personality.py        # Personality & mood system
├── expression.py         # Typing styles, emojis, reactions
├── relationships.py      # User relationship & trust scoring
├── image_gen.py          # Image generation (DALL-E, Stable Diffusion)
├── languages.py          # Multi-language support
├── conversation.py       # Conversation scoring & self-reflection
├── scheduler.py          # Scheduled events & behaviors
├── monitor.py            # Health checks, logs, uptime
├── env_manager.py        # Secure env variable editing
├── plugins.py            # Plugin system for custom skills
├── db.py                 # SQLAlchemy async setup
└── models.py             # Database models
```

## Dashboard Features

### 🔧 Engine Tab
- Switch between Ollama (local) and OpenAI (cloud)
- Manual generation with prompt input
- Real-time engine status

### 🎭 Personality Tab
- Set server personality preset
- Switch moods dynamically
- View current mood settings

### 💾 Memory Tab
- Add/list/delete memories
- Importance scoring
- Export/import memory data
- Memory decay simulation

### 🖼️ Images Tab
- Generate images using DALL-E or local models
- Style selection
- Base64 or URL output

### 👥 Relationships Tab
- View user relationship scores
- Trust/affinity levels
- Friend/enemy bias detection
- Export relationship data

### 📊 Monitoring Tab
- Real-time CPU/Memory/Disk usage
- Uptime tracking
- Log viewer (last N logs)
- Restart controls
- Health check status

### 🌐 Language Tab
- View available languages (en, es, fr, de, ja + custom)
- Set per-server language
- Set per-user language

### 🔌 Plugins Tab
- Load/unload plugins
- Execute custom skills
- View loaded plugins

### ⚙️ Config Tab
- View all environment variables (masked)
- Edit environment variables securely
- Reload .env file

## Discord Bot Commands

### Slash Commands
- `/ai_chat <prompt>` - Chat with AI
- `/engine_status` - Show current engine
- `/switch_engine <engine>` - Switch to ollama/openai
- `/generate_image <prompt>` - Generate image
- `/memory_add <key> <value>` - Save memory about user
- `/memory_list` - View your memories
- `/personality_show` - Show server personality
- `/set_mood <mood>` - Change bot mood

### Text Commands
- `!ping` - Pong
- `!status` - Show engine status (admin only)

### Auto Reactions
- Bot auto-reacts to mentions with mood-based emojis
- Reactions vary by mood and message context

## API Endpoints

### AI Generation
- `POST /generate` - Generate text with current engine
- `GET /status` - Get current engine info
- `POST /switch_engine/{name}` - Switch engines

### Memory
- `POST /memory` - Add memory
- `GET /memory/{owner}` - List memories
- `DELETE /memory/{mem_id}` - Delete memory
- `POST /memory/{owner}/export` - Export all memories
- `POST /memory/{owner}/import` - Import memories
- `POST /memory/decay` - Run decay algorithm

### Personality
- `GET /personality/presets` - List personality presets
- `POST /personality/override/{server_id}` - Set custom profile
- `GET /personality/{server_id}` - Get personality for server
- `POST /personality/{server_id}/mood` - Set mood

### Expression
- `GET /expression/emojis/{mood}` - Get emojis for mood
- `POST /expression/apply_mood` - Apply mood expression to text

### Relationships
- `GET /relationship/{user_id}` - Get relationship score
- `POST /relationship/{user_id}/update` - Update relationship
- `GET /relationships/export` - Export all relationships

### Images
- `POST /image/generate` - Generate image

### Languages
- `GET /languages` - List languages
- `POST /language/server/{server_id}` - Set server language
- `POST /language/user/{user_id}` - Set user language

### Monitoring
- `GET /health` - Full health check
- `GET /uptime` - Uptime info
- `GET /logs?limit=N` - Get recent logs
- `GET /metrics` - CPU/Memory/Disk stats
- `POST /restart` - Restart bot

### Environment
- `GET /env` - Get all env vars (masked)
- `POST /env/{key}` - Set env variable
- `POST /env/reload` - Reload .env file

### Plugins
- `GET /plugins` - List loaded plugins
- `POST /plugin/load/{name}` - Load plugin
- `POST /plugin/unload/{name}` - Unload plugin
- `POST /plugin/{name}/skill/{skill}` - Execute skill

### WebSocket
- `ws://localhost:8000/ws` - Real-time updates and commands

## Environment Variables

```
# Discord
DISCORD_BOT_TOKEN=your_token_here

# OpenAI (for cloud fallback)
OPENAI_API_KEY=your_key_here

# Ollama (local LLM)
OLLAMA_BASE=http://localhost:11434
OLLAMA_MODEL=llama2

# Database
DATABASE_URL=sqlite+aiosqlite:///./data.db

# Server
PORT=8000

# Directories
LOG_DIR=/workspaces/y/logs
PLUGIN_DIR=/workspaces/y/plugins
LANGUAGE_DIR=/workspaces/y/languages
FRONTEND_DIR=/workspaces/y/frontend
```

## Plugin Development

Create a file in `/workspaces/y/plugins/` named `my_plugin.py`:

```python
from backend.plugins import Plugin

class Plugin(Plugin):
    def __init__(self):
        super().__init__("my_plugin", "1.0")
        self.register_skill("my_skill", self.my_skill)

    async def on_load(self):
        print("Plugin loaded!")

    async def on_unload(self):
        print("Plugin unloaded!")

    async def my_skill(self, param: str) -> str:
        return f"Result: {param}"
```

Then via API:
```bash
curl -X POST http://localhost:8000/plugin/load/my_plugin
curl -X POST http://localhost:8000/plugin/my_plugin/skill/my_skill \
  -H "Content-Type: application/json" \
  -d '{"param":"value"}'
```

## Memory System

The bot maintains multiple types of memories:

1. **User Memory**: Facts about individual users (e.g., favorite color)
2. **Server Memory**: Rules, culture, inside jokes for specific servers
3. **Emotional Memory**: How users make the bot feel
4. **Temporary Context Memory**: Current conversation context

### Decay System
Older memories lose importance over time (configurable, default 30 days). This prevents the bot from being stuck in the past.

### Importance Scoring
Each memory has a weight (0-100) that affects how much it influences the bot's responses.

## Personality System

### Moods
- **Happy** 😊: High emoji use, exclamation marks, fast typing
- **Neutral** 😐: Minimal expression, balanced tone
- **Sad** 😢: Slow typing, fewer emojis, somber tone
- **Angry** 😠: ALL CAPS sometimes, heavy emoji, aggressive
- **Playful** 😄: Maximum emoji, random caps, joking tone
- **Focused** 🎯: Professional, minimal distraction

### Expression
Text is modified based on current mood:
- Capitalization varies
- Emoji frequency changes
- Exclamation mark usage
- Typing speed simulation

## Relationship Scoring

Each user has a relationship score tracking:
- **Trust** (0-100): How much the bot trusts this user
- **Affinity** (0-100): How much the bot likes this user
- **Interaction Count**: Total interactions
- **Friend Bias**: Auto-set when trust/affinity > 80
- **Enemy Bias**: Auto-set when trust/affinity < 30

Relationships decay over time when inactive.

## Troubleshooting

### Bot doesn't start
```bash
# Check logs
tail -f logs/bot.log

# Verify Discord token is set
cat .env | grep DISCORD_BOT_TOKEN
```

### Ollama connection fails
```bash
# Verify Ollama is running
curl http://localhost:11434/api/status

# Start Ollama if not running
ollama serve
```

### Database issues
```bash
# Delete and recreate
rm data.db
# Restart bot
```

### Memory leaks
The memory decay system runs automatically. To force decay:
```bash
curl -X POST http://localhost:8000/memory/decay \
  -H "Content-Type: application/json" \
  -d '{"days":30}'
```

## Advanced: Scheduled Behaviors

You can register scheduled events to run automatically:

```python
# In your plugin
from backend.scheduler import scheduler, ScheduledEvent

async def daily_greeting():
    print("Good morning!")

event = ScheduledEvent("greet", "time", daily_greeting, interval_seconds=86400)
await scheduler.register(event)
```

## Performance Optimization

1. **Async Everywhere**: All I/O is non-blocking
2. **Connection Pooling**: HTTP client reuses connections
3. **Memory Management**: Old memories decay and can be pruned
4. **Caching**: Personality profiles cached per-server
5. **Rate Limiting**: Implement via dashboard if needed

## Security Notes

1. **Environment Variables**: Sensitive keys masked in `/env` endpoint
2. **Database**: SQLite is file-based; use PostgreSQL in production
3. **Dashboard**: No authentication currently; add before production
4. **Plugins**: Load only trusted plugins
5. **API Rate Limiting**: Not implemented; add middleware before production

## Next Steps (Roadmap)

- [ ] Dashboard authentication (2FA)
- [ ] PostgreSQL support
- [ ] GPU monitoring and allocation
- [ ] Voice channel presence
- [ ] Advanced self-reflection with scoring
- [ ] Multi-agent reasoning (CoT)
- [ ] Custom LLM fine-tuning
- [ ] Encrypted memory storage
- [ ] Permission system (RBAC)
- [ ] Analytics and statistics dashboard

## Support & Contributing

For issues, enhancements, or feature requests, refer to the main README.

---

**Last Updated**: January 2026
**Version**: 1.0.0
