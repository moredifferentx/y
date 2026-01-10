# Troubleshooting Guide

## Installation Issues

### Virtual Environment Not Creating
```bash
# Manually create venv
python3 -m venv /workspaces/y/.venv
source /workspaces/y/.venv/bin/activate
pip install -r requirements.txt
```

### Dependency Installation Fails
```bash
# Update pip first
pip install --upgrade pip setuptools wheel

# Try installing one at a time to identify problem
pip install fastapi
pip install discord.py
# etc...
```

### Python Version Mismatch
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Use specific Python path if multiple versions exist
/usr/bin/python3.11 -m venv .venv
```

---

## Discord Bot Issues

### Bot Won't Connect
```bash
# Check Discord token is set
grep "DISCORD_BOT_TOKEN" .env

# Verify token format (should be long string)
# If empty or starting with "your_", update .env

# Check token is valid
# Go to: https://discord.com/developers/applications
# Verify bot hasn't been revoked
```

### Bot Doesn't Respond to Commands
```bash
# Check message content intent is enabled
# Dashboard → Settings → Privileged Gateway Intents
# Toggle on "Message Content Intent"

# Check bot has permissions in server
# Right-click bot in Discord → Manage → Permissions
# Ensure "Send Messages", "Read Messages", "Manage Reactions"

# Check bot role is positioned above users
# Server Settings → Roles → Move bot role up
```

### Slash Commands Don't Show Up
```bash
# Bot might need re-invite
# Get new invite URL with slash commands:
# https://discordapp.com/oauth2/authorize?client_id=YOUR_ID&scope=bot%20applications.commands

# Force command sync
# Restart bot completely
./start.sh  # This will trigger sync on startup
```

### "Application not found" Error
```bash
# Invite bot with correct scopes
# Go to: Discord Developer Portal → OAuth2 → URL Generator
# Select: bot + applications.commands
# Copy URL and use to invite bot

# Make sure bot is in the server first!
```

---

## LLM Connection Issues

### Ollama Connection Failed
```bash
# Check if Ollama is running
curl http://localhost:11434/api/status

# Start Ollama if not running
ollama serve

# In another terminal, pull a model if needed
ollama pull llama2

# If OLLAMA_BASE in .env is wrong, update it
grep OLLAMA_BASE .env
# Should be: http://localhost:11434
```

### Ollama Model Not Found
```bash
# See available models
ollama list

# Pull a model
ollama pull llama2
ollama pull neural-chat

# Set default model in .env
# OLLAMA_MODEL=llama2
```

### Ollama Timeout
```bash
# Increase timeout in backend/ai/ollama_client.py
# Change timeout=30.0 to timeout=60.0

# Or restart Ollama - sometimes it needs restart
killall ollama
ollama serve
```

### OpenAI API Fails
```bash
# Check API key is set
grep OPENAI_API_KEY .env

# Verify key format (starts with sk-)
# Get new key from: https://platform.openai.com/api_keys

# Check account has credits
# Visit: https://platform.openai.com/account/billing/overview

# Check rate limit (if key shares quota with other apps)
# Visit: https://platform.openai.com/account/rate-limits
```

---

## Database Issues

### Database Locked Error
```bash
# Close all bot instances
pkill -f "python.*backend.app"

# Wait a few seconds
sleep 2

# Restart bot
./start.sh
```

### Database Corruption
```bash
# Backup old database
mv data.db data.db.backup

# Start bot (will create fresh database)
./start.sh

# Bot will reinitialize empty database
# Previous memories will be lost
```

### Can't Read Memory
```bash
# Check memory owner is correct
curl http://localhost:8000/memory/user_123

# If empty, add some memory first
curl -X POST http://localhost:8000/memory \
  -H "Content-Type: application/json" \
  -d '{"owner":"user_123","key":"test","value":"hello"}'
```

---

## Dashboard Issues

### Dashboard Blank or Won't Load
```bash
# Check frontend files exist
ls -la frontend/index.html

# Check FastAPI is running
curl http://localhost:8000/

# Check port (default 8000)
lsof -i :8000

# If port in use, change PORT in .env
PORT=8001 ./start.sh
```

### WebSocket Connection Failed
```bash
# Check WebSocket URL is correct
# Dashboard connects to: ws://localhost:8000/ws

# Check if behind proxy/firewall
# Some proxies don't support WebSocket

# If over HTTPS, use wss:// instead of ws://
```

### Metrics Not Updating
```bash
# Check psutil is installed
pip list | grep psutil

# Restart bot
./start.sh

# Check /metrics endpoint manually
curl http://localhost:8000/metrics
```

### Buttons/Forms Not Working
```bash
# Check browser console for errors (F12)
# Likely JavaScript issue

# Verify API is running
curl http://localhost:8000/

# Try different browser (Firefox vs Chrome)
```

---

## Performance Issues

### Bot Slow to Respond
```bash
# Check which engine is active
curl http://localhost:8000/status

# If using Ollama, model might be loading
# Wait for model to load (first request can take 10+ seconds)

# Check system resources
free -h  # Memory
df -h    # Disk space
top      # CPU

# Switch to OpenAI if Ollama is slow
curl -X POST http://localhost:8000/switch_engine/openai
```

### High Memory Usage
```bash
# Check current memory
curl http://localhost:8000/metrics

# Run memory decay
curl -X POST http://localhost:8000/memory/decay \
  -H "Content-Type: application/json" \
  -d '{"days":30}'

# Restart bot to free memory
curl -X POST http://localhost:8000/restart
```

### Slow Dashboard Updates
```bash
# Check network tab in browser (F12)
# Identify slow API calls

# If /metrics is slow:
# - Check system load
# - Reduce update frequency in dashboard

# If memory list is slow:
# - Too many memories (1000+)
# - Archive old ones or export/delete
```

---

## Plugin Issues

### Plugin Won't Load
```bash
# Check plugin file exists and is in correct location
ls -la plugins/my_plugin.py

# Check plugin has correct structure
# Must have "class Plugin(Plugin):" 

# Check plugin for syntax errors
python3 -m py_compile plugins/my_plugin.py

# Check logs for error details
tail -f logs/bot.log
```

### Plugin Skill Execution Fails
```bash
# Test plugin load first
curl -X POST http://localhost:8000/plugin/load/my_plugin

# Check plugin is loaded
curl http://localhost:8000/plugins

# Verify skill name is correct
# Execute with correct parameters
curl -X POST http://localhost:8000/plugin/my_plugin/skill/my_skill \
  -H "Content-Type: application/json" \
  -d '{"param":"value"}'
```

---

## Logs & Debugging

### View Recent Logs
```bash
# Last 50 lines
tail -50 logs/bot.log

# Follow in real-time
tail -f logs/bot.log

# Search for errors
grep ERROR logs/bot.log

# Get logs via API
curl http://localhost:8000/logs?limit=100
```

### Enable Debug Logging
```bash
# Edit backend/app.py
# Add near top:
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export LOGLEVEL=DEBUG
./start.sh
```

### Check Event Logs
```bash
# View scheduled events
curl http://localhost:8000/scheduler/events

# View health status
curl http://localhost:8000/health

# View current metrics
curl http://localhost:8000/metrics
```

---

## Environment Variable Issues

### Variable Changes Not Taking Effect
```bash
# Edit .env
nano .env

# Reload environment
curl -X POST http://localhost:8000/env/reload

# Or restart bot
./start.sh
```

### Can't See Sensitive Variables
```bash
# This is intentional for security!
# API masks variables with "API_KEY", "TOKEN", "SECRET"

# To view the actual value:
source .env
echo $DISCORD_BOT_TOKEN

# Or edit .env directly
cat .env | grep DISCORD
```

### Environment Variable Format Error
```bash
# Variables must be UPPERCASE_WITH_UNDERSCORES
# Format: KEY=value (no spaces around =)

# Check .env format
cat .env

# Common issues:
# - Spaces: KEY = value  (wrong)
# - Quotes: KEY="value"  (usually OK but not needed)
# - Newlines: missing newline at end of file (add one)
```

---

## Port/Network Issues

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
PORT=8001 ./start.sh
```

### Can't Access Dashboard from Other Machine
```bash
# Check if 0.0.0.0 binding in app.py
# Currently binds to 0.0.0.0:8000 (all interfaces)

# If behind firewall, open port 8000
# iptables -A INPUT -p tcp --dport 8000 -j ACCEPT

# From another machine, use server IP
http://YOUR_SERVER_IP:8000/static/index.html
```

### SSL/HTTPS Certificate Issues
```bash
# Dashboard runs on HTTP by default
# For HTTPS, use reverse proxy (nginx, apache)

# Example with nginx:
# - Proxy localhost:8000
# - Handle SSL with certbot
# - Visit https://your-domain.com
```

---

## Common Error Messages

### "Connection refused"
```
Problem: Bot can't connect to Ollama or API
Solution: Check OLLAMA_BASE in .env, verify Ollama running
```

### "401 Unauthorized"
```
Problem: OpenAI API key invalid or missing
Solution: Verify OPENAI_API_KEY in .env, get new key if needed
```

### "Database is locked"
```
Problem: Multiple bot instances or unclean shutdown
Solution: Kill all instances, restart bot, check for zombie processes
```

### "No module named 'discord'"
```
Problem: discord.py not installed
Solution: pip install discord.py
```

### "Slash commands not appearing"
```
Problem: Bot doesn't have applications.commands scope
Solution: Re-invite bot with correct OAuth2 scope, enable Message Content Intent
```

---

## Getting Help

### Check Logs
```bash
tail -f logs/bot.log
```

### Test API Directly
```bash
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/status
```

### Check System Status
```bash
# See what's running
ps aux | grep python

# Check ports
netstat -tuln | grep LISTEN

# Check disk space
df -h

# Check memory
free -h
```

### Enable Verbose Mode
```bash
# Set log level to DEBUG
export LOGLEVEL=DEBUG
./start.sh

# Or modify backend/app.py:
# logging.basicConfig(level=logging.DEBUG)
```

---

## Still Stuck?

1. Check all logs: `tail -f logs/bot.log`
2. Verify configuration: `cat .env | grep -v "^#"`
3. Test endpoints: `curl http://localhost:8000/health`
4. Check Discord permissions: Right-click bot → roles
5. Verify Ollama running: `curl http://localhost:11434/api/status`
6. Check system resources: `free -h && df -h`
7. Restart everything from scratch: `./start.sh`

---

**Last Updated**: January 2026  
**Version**: 1.0.0
