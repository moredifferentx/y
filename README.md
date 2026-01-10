# Discord AI — Hybrid Local+Cloud Chatbot (Production-Grade)

A **complete, feature-rich Discord AI chatbot** with local LLM (Ollama) + cloud fallback (OpenAI), full dashboard control, human-like behavior, memory system, personality engine, image generation, and more.

## 🚀 Quick Start

```bash
cp .env.example .env
# Edit .env with your Discord bot token and OpenAI key
chmod +x start.sh
./start.sh
```

Open dashboard: `http://localhost:8000/static/index.html`

## ✨ Features

### 🤖 Hybrid AI Engine
- **Primary**: Local Ollama LLM (fast, private, on-device)
- **Fallback**: Cloud OpenAI API (reliable, powerful)
- **Hot-swappable**: Switch engines without restarting
- **Isolated**: No shared state conflicts
- **Metrics**: Latency, throughput, error rates

### 👥 Human-Like Behavior
- **Personality System**: 6 mood types (happy, sad, angry, playful, focused, neutral)
- **Expression Engine**: Mood-based typing speed, emoji usage, capitalization
- **Memory System**: Long-term user/server memories with decay and importance scoring
- **Relationship Scoring**: Trust/affinity levels, friend/enemy bias detection
- **Auto Reactions**: Emoji reactions based on mood and message context

### 🎭 Personality & Mood
- **6 Preset Personalities**: Friendly, logical, chaotic, calm, creative, professional
- **Per-Server Overrides**: Different personality per Discord server
- **Dynamic Mood**: Changes based on interactions, admin commands, or time
- **Mood Effects**: Response length, emoji usage, tone, typing speed

### 💾 Memory System
- **Multiple Types**: User, server, emotional, conversational
- **Importance Scoring**: Prioritize memorable events
- **Memory Decay**: Older memories lose relevance over time
- **Export/Import**: Backup and restore memories
- **Full Dashboard Control**: Add, edit, delete memories from UI

### 🖼️ Image Generation
- **Local Models**: Stable Diffusion via Ollama (if available)
- **Cloud Fallback**: DALL-E via OpenAI
- **Style Selection**: Anime, oil painting, photography, etc.
- **Discord Commands**: `/generate_image <prompt>`
- **Base64 & URLs**: Both formats supported

### 🌐 Multi-Language Support
- **Built-in**: English, Spanish, French, German, Japanese
- **Custom Languages**: Upload JSON language files
- **Per-Server & Per-User**: Different language per context
- **Auto-Detection**: Optional language detection

### 📊 System Monitoring
- **Real-Time Metrics**: CPU, Memory, Disk usage
- **Uptime Tracking**: Continuous monitoring with restart count
- **Health Checks**: Automatic system health status
- **Live Logs**: View recent logs in dashboard
- **Restart Controls**: Graceful restart from dashboard

### 🔌 Plugin System
- **Custom Skills**: Inject custom functionality
- **Hot-Load**: Load/unload plugins without restart
- **Async Ready**: Full async/await support
- **Example Plugin**: See `plugins/hello_skill.py`

### 📋 Full Dashboard Control
- **Engine Switching**: Toggle between Ollama and OpenAI
- **Personality Management**: Edit mood, personality presets
- **Memory CRUD**: Add, list, delete, export memories
- **Relationship Viewer**: See trust/affinity scores
- **Configuration**: Edit environment variables securely
- **Monitoring**: CPU, Memory, Disk, Logs, Health
- **Language Settings**: Change language per server/user
- **Plugin Manager**: Load/unload plugins and execute skills

### 🎮 Discord Bot Commands

**Slash Commands** (modern Discord):
- `/ai_chat <prompt>` - Chat with AI
- `/engine_status` - Show current engine
- `/switch_engine <engine>` - Switch to ollama/openai
- `/generate_image <prompt>` - Generate image
- `/memory_add <key> <value>` - Save memory
- `/memory_list` - View your memories
- `/personality_show` - Show bot personality
- `/set_mood <mood>` - Change bot mood

**Text Commands**:
- `!ping` - Ping response
- `!status` - Show engine status (admin)

**Auto Reactions**:
- Bot auto-reacts to mentions with mood-based emojis

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py                 # Main FastAPI app (all endpoints)
│   ├── ai/
│   │   ├── engine.py         # AI engine manager
│   │   ├── ollama_client.py  # Local LLM
│   │   └── cloud_client.py   # Cloud LLM (OpenAI)
│   ├── bot/
│   │   └── discord_bot.py    # Discord bot (slash commands, reactions)
│   ├── memory.py             # Memory store
│   ├── personality.py        # Personality & mood
│   ├── expression.py         # Typing styles & emoji reactions
│   ├── relationships.py      # User relationship scoring
│   ├── image_gen.py          # Image generation
│   ├── languages.py          # Multi-language support
│   ├── conversation.py       # Conversation quality scoring
│   ├── scheduler.py          # Scheduled events
│   ├── monitor.py            # System monitoring & health
│   ├── env_manager.py        # Environment variable management
│   ├── plugins.py            # Plugin system
│   ├── db.py                 # Database setup
│   └── models.py             # Database models
├── frontend/
│   └── index.html            # Full-featured dashboard
├── plugins/
│   └── hello_skill.py        # Example plugin
├── languages/                # Custom language files (JSON)
├── logs/                     # Application logs
├── start.sh                  # One-command launcher
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Setup Instructions

### 1. Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai) installed (for local LLM)
- Discord server with admin permissions
- OpenAI API key (optional, for cloud fallback)

### 2. Configuration

```bash
cp .env.example .env
```

Edit `.env`:
```
DISCORD_BOT_TOKEN=your_discord_bot_token
OPENAI_API_KEY=sk-...  # optional
OLLAMA_BASE=http://localhost:11434
OLLAMA_MODEL=llama2
PORT=8000
```

### 3. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Go to **Bot** tab → **Add Bot**
4. Copy token to `.env`
5. Enable **Message Content Intent** under Privileged Gateway Intents
6. Go to **OAuth2** → **URL Generator**
7. Select scopes: `bot`
8. Select permissions: `Send Messages`, `Read Messages`, `Manage Reactions`, `Slash Commands`
9. Copy generated URL and invite bot to your server

### 4. Local LLM Setup (Ollama)

```bash
# Install Ollama from https://ollama.ai
# Run Ollama service
ollama serve

# In another terminal, pull a model
ollama pull llama2
```

### 5. Start Everything

```bash
chmod +x start.sh
./start.sh
```

**What it does:**
- Creates Python virtual environment
- Installs dependencies
- Initializes SQLite database
- Starts FastAPI backend (port 8000)
- Starts Discord bot (async, no blocking)
- Ready to use!

### 6. Access Dashboard

Open: `http://localhost:8000/static/index.html`

## 📖 Documentation

- **[Full Documentation](./FULL_DOCUMENTATION.md)** - Complete guide with all features, API endpoints, and advanced usage
- **[Environment Variables](./README.md#-setup-instructions)** - Configuration reference
- **[Plugin Development](./FULL_DOCUMENTATION.md#plugin-development)** - Create custom skills
- **[Troubleshooting](./FULL_DOCUMENTATION.md#troubleshooting)** - Common issues and fixes

## 🌟 Key Technologies

- **FastAPI**: Modern, fast web framework
- **Discord.py**: Official Discord library with slash commands
- **SQLAlchemy**: Async ORM for database
- **SQLite**: Lightweight embedded database
- **Ollama**: Local LLM inference
- **OpenAI**: Cloud LLM fallback
- **httpx**: Async HTTP client
- **psutil**: System monitoring

## 💡 Advanced Features

### Hybrid LLM Architecture
Seamlessly switch between local (Ollama) and cloud (OpenAI) engines:
- **Local**: Fast, private, no API costs
- **Cloud**: More powerful, up-to-date knowledge
- **Fallback**: Automatic failover if primary fails
- **Manual Override**: Force engine via dashboard

### Memory with Decay
- **Importance Scoring**: 0-100 weight for each memory
- **Decay Algorithm**: Older memories lose relevance
- **Export/Import**: Backup and restore
- **Full Control**: View, edit, delete from dashboard

### Personality Engine
- **Mood System**: 6 distinct moods affecting behavior
- **Expression Variation**: Typing speed, emoji use, tone changes
- **Per-Server Profiles**: Different personality per Discord server
- **Auto-Reactions**: Context-aware emoji reactions

### Relationship Scoring
- **Trust & Affinity**: Tracks per-user relationship
- **Friend/Enemy Bias**: Subtle behavioral changes
- **Interaction Tracking**: Counts and timestamps
- **Decay System**: Relationships fade without interaction

### System Health & Monitoring
- **Uptime Tracking**: From startup
- **Resource Monitoring**: CPU, Memory, Disk %
- **Health Checks**: Automated status monitoring
- **Live Logs**: Stream recent application logs
- **Restart Control**: Graceful bot restart

### Plugin System
- **Custom Skills**: Extend bot functionality
- **Hot-Loading**: Load plugins without restart
- **API Execution**: Run skills via REST API
- **Examples**: See `plugins/hello_skill.py`

## 🔐 Security Considerations

⚠️ **Before Production Deployment:**
- [ ] Add dashboard authentication (2FA recommended)
- [ ] Move to PostgreSQL (from SQLite)
- [ ] Implement API rate limiting
- [ ] Encrypt sensitive memory data
- [ ] Use environment secrets manager
- [ ] Audit permission system
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging and monitoring

## 📊 Performance

- **Async I/O**: All network operations are non-blocking
- **Connection Pooling**: HTTP clients reuse connections
- **Memory Efficient**: Old memories decay automatically
- **GPU Support**: Can leverage GPU if available (Ollama config)
- **Horizontal Scaling**: Stateless backend, can be load-balanced

## 🐛 Troubleshooting

**Bot won't start:**
```bash
tail -f logs/bot.log
# Check .env has DISCORD_BOT_TOKEN
```

**Ollama connection fails:**
```bash
curl http://localhost:11434/api/status
# Start Ollama: ollama serve
```

**Database errors:**
```bash
rm data.db
# Restart bot to reinitialize
```

## 📚 Learn More

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [Ollama Models](https://ollama.ai/library)
- [OpenAI API](https://platform.openai.com/docs)

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 🚀 Roadmap

- [ ] Dashboard authentication
- [ ] PostgreSQL support
- [ ] GPU monitoring dashboard
- [ ] Voice channel presence
- [ ] Advanced reasoning (CoT, multi-agent)
- [ ] Fine-tuning system
- [ ] Encrypted memory
- [ ] RBAC permissions
- [ ] Analytics dashboard
- [ ] Docker containerization

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Status**: Production-Ready with caveats (see Security section)
# y