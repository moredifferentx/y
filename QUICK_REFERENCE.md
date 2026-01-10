# Quick Reference Card

## 🚀 Getting Started (30 seconds)

```bash
cd /workspaces/y
cp .env.example .env
# Edit .env: add DISCORD_BOT_TOKEN and OPENAI_API_KEY (optional)
./start.sh
```

Open: `http://localhost:8000/static/index.html`

## 🎯 Key Commands

### Start Everything
```bash
./start.sh
```

### Stop Bot
```bash
Ctrl+C
```

### Check Status
```bash
curl http://localhost:8000/status
```

### View Logs
```bash
tail -f logs/bot.log
```

### Restart (graceful)
```bash
curl -X POST http://localhost:8000/restart
```

## 💻 API Endpoints (Top 10)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/generate` | POST | Generate AI text |
| `/switch_engine/{name}` | POST | Switch Ollama/OpenAI |
| `/memory` | POST | Add memory |
| `/memory/{owner}` | GET | List memories |
| `/personality/{server_id}/mood` | POST | Set mood |
| `/image/generate` | POST | Generate image |
| `/relationship/{user_id}` | GET | Get relationship score |
| `/health` | GET | System health |
| `/metrics` | GET | CPU/Memory/Disk |
| `/ws` | WS | Real-time updates |

## 🎮 Discord Commands

- `/ai_chat <prompt>` - Chat with AI
- `/engine_status` - Show current engine
- `/set_mood <mood>` - Change mood (happy/sad/angry/playful/focused/neutral)
- `/generate_image <prompt>` - Generate image
- `/memory_add <key> <value>` - Save memory
- `!ping` - Ping

## 🔧 Environment Variables

```
DISCORD_BOT_TOKEN=your_token_here
OPENAI_API_KEY=sk-...
OLLAMA_BASE=http://localhost:11434
OLLAMA_MODEL=llama2
PORT=8000
```

## 📊 Dashboard Tabs

1. **🔧 Engine** - Switch engines, generate text
2. **🎭 Personality** - Mood control, personality profiles
3. **💾 Memory** - Add/list/export memories
4. **🖼️ Images** - Generate images with AI
5. **👥 Relationships** - View user trust/affinity scores
6. **📊 Monitoring** - CPU/Memory, logs, health
7. **🌐 Language** - Set language per server/user
8. **🔌 Plugins** - Load custom skills
9. **⚙️ Config** - Edit environment variables

## 🐛 Troubleshooting

### Bot won't connect to Discord
```bash
# Check token
grep DISCORD_BOT_TOKEN .env

# Check bot has required intents in Discord Developer Portal
# Enable: Message Content Intent
```

### Can't reach Ollama
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/status
```

### Port 8000 already in use
```bash
# Use different port
PORT=8001 ./start.sh

# Or kill process using port
lsof -i :8000  # Find PID
kill -9 <PID>
```

### Database locked
```bash
# Kill all bot instances
pkill -f "python.*backend.app"

# Restart
./start.sh
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Main API (40+ endpoints) |
| `backend/bot/discord_bot.py` | Discord bot logic |
| `backend/memory.py` | Memory storage |
| `backend/personality.py` | Mood & personality |
| `frontend/index.html` | Dashboard UI |
| `.env` | Configuration (create from .env.example) |
| `start.sh` | One-command launcher |

## 🔌 Create Plugin (5 minutes)

1. Create file: `plugins/my_plugin.py`

```python
from backend.plugins import Plugin

class Plugin(Plugin):
    def __init__(self):
        super().__init__("my_plugin", "1.0")
        self.register_skill("my_skill", self.my_skill)

    async def my_skill(self, text: str) -> str:
        return f"Processed: {text}"
```

2. Load via API:
```bash
curl -X POST http://localhost:8000/plugin/load/my_plugin
```

3. Execute:
```bash
curl -X POST http://localhost:8000/plugin/my_plugin/skill/my_skill \
  -H "Content-Type: application/json" \
  -d '{"text":"hello"}'
```

## 🌍 Supported Languages

- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese

Add custom: Create JSON file in `/workspaces/y/languages/`

## 📈 Performance Tips

- Switch to OpenAI if Ollama is slow
- Run memory decay periodically: `POST /memory/decay`
- Monitor metrics: `GET /metrics`
- Check logs for errors: `tail -f logs/bot.log`

## 🔐 Security Checklist (Before Production)

- [ ] Add dashboard authentication
- [ ] Enable HTTPS/SSL
- [ ] Add API rate limiting
- [ ] Use PostgreSQL instead of SQLite
- [ ] Encrypt sensitive memories
- [ ] Set up proper logging & monitoring
- [ ] Enable input validation

## 📚 Documentation

- **README.md** - Overview & quick start
- **FULL_DOCUMENTATION.md** - Complete guide
- **API_REFERENCE.md** - All endpoints
- **TROUBLESHOOTING.md** - Common issues
- **IMPLEMENTATION_SUMMARY.md** - Features & customization

## 💡 Pro Tips

1. **Faster generation**: Use OpenAI instead of Ollama
2. **Better personality**: Edit personality presets per server
3. **Memory management**: Run decay regularly to keep memories relevant
4. **Custom behavior**: Create plugins for specialized tasks
5. **Monitor health**: Check `/health` endpoint regularly

## ⚡ API Quick Test

```bash
# Test API is working
curl http://localhost:8000/health

# Generate text
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello!"}'

# Check engine
curl http://localhost:8000/status

# Switch engine
curl -X POST http://localhost:8000/switch_engine/openai
```

## 🎯 Common Use Cases

### Add Memory About User
```bash
curl -X POST http://localhost:8000/memory \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "user_123",
    "key": "favorite_color",
    "value": "blue"
  }'
```

### Set Bot Mood
```bash
curl -X POST http://localhost:8000/personality/server_456/mood \
  -H "Content-Type: application/json" \
  -d '{"mood": "playful"}'
```

### Generate Image
```bash
curl -X POST http://localhost:8000/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a cute cat",
    "style": "anime"
  }'
```

### Export All Memories
```bash
curl http://localhost:8000/memory/user_123/export -X POST
```

## 📞 Support

- Check logs: `tail -f logs/bot.log`
- Test API: `curl http://localhost:8000/docs` (interactive docs)
- Read docs: Check TROUBLESHOOTING.md
- Check Discord: Verify bot permissions and intents

---

**Version**: 1.0.0 | **Status**: Production Ready | **Last Updated**: January 2026

Print this page as a reference! 🖨️
