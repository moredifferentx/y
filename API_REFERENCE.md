# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication. Before production, add JWT or OAuth2.

## Response Format

All responses are JSON. Errors return appropriate HTTP status codes.

```json
{
  "ok": true,
  "data": {...}
}
```

---

## AI Generation

### Generate Text

Generate text using the currently active AI engine.

**Request:**
```
POST /generate
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "meta": {
    "user_id": "12345",
    "context": "dm"
  }
}
```

**Response:**
```json
{
  "text": "I'm doing great, thanks for asking!"
}
```

### Get Engine Status

Check which engine is currently active.

**Request:**
```
GET /status
```

**Response:**
```json
{
  "engine": "ollama",
  "engines": ["ollama", "openai"]
}
```

### Switch Engine

Switch between Ollama (local) and OpenAI (cloud).

**Request:**
```
POST /switch_engine/openai
```

**Response:**
```json
{
  "ok": true,
  "engine": "openai"
}
```

---

## Memory Management

### Add Memory

Store a memory about a user or server.

**Request:**
```
POST /memory
Content-Type: application/json

{
  "owner": "user_123",
  "key": "favorite_color",
  "value": "blue",
  "importance": 0.8
}
```

**Response:**
```json
{
  "ok": true,
  "id": 42
}
```

### List Memories

Retrieve all memories for an owner.

**Request:**
```
GET /memory/user_123
```

**Response:**
```json
[
  {
    "id": 42,
    "key": "favorite_color",
    "value": "blue",
    "importance": 0.8,
    "created_at": "2026-01-10T12:00:00"
  }
]
```

### Delete Memory

Remove a specific memory.

**Request:**
```
DELETE /memory/42
```

**Response:**
```json
{
  "ok": true
}
```

### Export Memories

Export all memories for an owner as JSON.

**Request:**
```
POST /memory/user_123/export
```

**Response:**
```json
{
  "ok": true,
  "data": "[{\"id\":42,\"key\":\"favorite_color\",\"value\":\"blue\",...}]"
}
```

### Import Memories

Import memories for an owner from JSON.

**Request:**
```
POST /memory/user_123/import
Content-Type: application/json

{
  "data": "[{\"id\":42,\"key\":\"favorite_color\",\"value\":\"blue\"}]"
}
```

**Response:**
```json
{
  "ok": true
}
```

### Run Memory Decay

Reduce importance of old memories.

**Request:**
```
POST /memory/decay
Content-Type: application/json

{
  "days": 30
}
```

**Response:**
```json
{
  "ok": true
}
```

---

## Personality & Mood

### List Personality Presets

Get available personality profiles.

**Request:**
```
GET /personality/presets
```

**Response:**
```json
{
  "presets": ["friendly", "logical", "chaotic"]
}
```

### Get Personality for Server

Retrieve the personality profile and mood for a server.

**Request:**
```
GET /personality/server_456
```

**Response:**
```json
{
  "profile": {
    "tone": "friendly",
    "emoji_use": 0.6,
    "formality": 0.3
  },
  "mood": "happy"
}
```

### Set Server Personality Override

Apply a custom personality profile to a server.

**Request:**
```
POST /personality/override/server_456
Content-Type: application/json

{
  "tone": "logical",
  "emoji_use": 0.1,
  "formality": 0.8
}
```

**Response:**
```json
{
  "ok": true
}
```

### Set Mood

Change the bot's mood for a server.

**Request:**
```
POST /personality/server_456/mood
Content-Type: application/json

{
  "mood": "playful"
}
```

**Response:**
```json
{
  "ok": true
}
```

Valid moods: `happy`, `neutral`, `sad`, `angry`, `playful`, `focused`

---

## Expression

### Get Emojis for Mood

Retrieve emoji set for a specific mood.

**Request:**
```
GET /expression/emojis/happy
```

**Response:**
```json
{
  "mood": "happy",
  "emojis": ["😊", "🎉", "😄", "✨", "🌟"]
}
```

### Apply Mood Expression

Modify text based on mood (capitalization, emojis, etc).

**Request:**
```
POST /expression/apply_mood
Content-Type: application/json

{
  "text": "hello world",
  "mood": "happy"
}
```

**Response:**
```json
{
  "original": "hello world",
  "transformed": "HELLO WORLD! ✨😊"
}
```

---

## Relationships

### Get User Relationship Score

Retrieve relationship metrics for a user.

**Request:**
```
GET /relationship/user_123
```

**Response:**
```json
{
  "user_id": "user_123",
  "trust": 75.5,
  "affinity": 68.2,
  "interaction_count": 42,
  "friend_bias": true,
  "enemy_bias": false
}
```

### Update Relationship

Modify relationship after an interaction.

**Request:**
```
POST /relationship/user_123/update
Content-Type: application/json

{
  "sentiment": 0.8,
  "is_positive": true
}
```

**Response:**
```json
{
  "user_id": "user_123",
  "trust": 78.5,
  "affinity": 71.2,
  "interaction_count": 43,
  "friend_bias": true,
  "enemy_bias": false
}
```

### Export All Relationships

Download all relationship data.

**Request:**
```
GET /relationships/export
```

**Response:**
```json
{
  "ok": true,
  "data": {
    "user_123": {...},
    "user_456": {...}
  }
}
```

---

## Image Generation

### Generate Image

Create an image using AI (DALL-E or local model).

**Request:**
```
POST /image/generate
Content-Type: application/json

{
  "prompt": "a cute cat wearing sunglasses",
  "style": "anime"
}
```

**Response:**
```json
{
  "ok": true,
  "image_url": "data:image/png;base64,iVBORw0KGgo..."
}
```

Styles: `default`, `anime`, `oil-painting`, `photography`

---

## Languages

### List Available Languages

Get all supported languages.

**Request:**
```
GET /languages
```

**Response:**
```json
{
  "en": "English",
  "es": "Spanish",
  "fr": "French",
  "de": "German",
  "ja": "Japanese"
}
```

### Set Server Language

Set the language for a Discord server.

**Request:**
```
POST /language/server/server_456
Content-Type: application/json

{
  "language": "es"
}
```

**Response:**
```json
{
  "ok": true
}
```

### Set User Language

Set the language for a specific user.

**Request:**
```
POST /language/user/user_123
Content-Type: application/json

{
  "language": "fr"
}
```

**Response:**
```json
{
  "ok": true
}
```

---

## Conversation Scoring

### Add Message to Conversation

Log a message for quality scoring.

**Request:**
```
POST /conversation/conv_123/add
Content-Type: application/json

{
  "role": "user",
  "content": "That was amazing!",
  "sentiment": 0.9
}
```

**Response:**
```json
{
  "ok": true
}
```

### Get Conversation Score

Evaluate conversation quality.

**Request:**
```
GET /conversation/conv_123/score
```

**Response:**
```json
{
  "id": "conv_123",
  "quality_score": 82.5,
  "sentiment_avg": 0.65,
  "engagement_score": 75.0,
  "reflection": "Great conversation! Good back-and-forth with 8 messages.",
  "message_count": 8
}
```

---

## System Monitoring

### Health Check

Get full system health status.

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "uptime_seconds": 3600,
  "uptime_human": "1:00:00",
  "start_time": "2026-01-10T12:00:00",
  "restart_count": 0,
  "last_error": null,
  "log_count": 42
}
```

### Get Uptime

Retrieve uptime information only.

**Request:**
```
GET /uptime
```

**Response:**
```json
{
  "uptime_seconds": 3600,
  "uptime_human": "1:00:00",
  "start_time": "2026-01-10T12:00:00",
  "restart_count": 0
}
```

### Get Metrics

Retrieve system resource metrics.

**Request:**
```
GET /metrics
```

**Response:**
```json
{
  "engine": "ollama",
  "cpu_percent": 25.3,
  "memory_percent": 45.8,
  "disk_percent": 32.1,
  "uptime_seconds": 3600
}
```

### Get Recent Logs

Retrieve application logs.

**Request:**
```
GET /logs?limit=50
```

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2026-01-10T12:30:45",
      "level": "INFO",
      "message": "Generated text for prompt"
    }
  ]
}
```

### Restart Bot

Trigger a graceful bot restart.

**Request:**
```
POST /restart
```

**Response:**
```json
{
  "ok": true,
  "restarting": true
}
```

---

## Environment Management

### Get Environment Variables

Retrieve all environment variables (sensitive ones are masked).

**Request:**
```
GET /env
```

**Response:**
```json
{
  "DISCORD_BOT_TOKEN": "***REDACTED***",
  "OPENAI_API_KEY": "***REDACTED***",
  "OLLAMA_BASE": "http://localhost:11434",
  "PORT": "8000"
}
```

### Set Environment Variable

Set or update an environment variable.

**Request:**
```
POST /env/OLLAMA_MODEL
Content-Type: application/json

{
  "value": "llama2-7b"
}
```

**Response:**
```json
{
  "ok": true
}
```

### Reload Environment

Reload all environment variables from .env file.

**Request:**
```
POST /env/reload
```

**Response:**
```json
{
  "ok": true
}
```

---

## Plugins

### List Plugins

Get all loaded plugins and their skills.

**Request:**
```
GET /plugins
```

**Response:**
```json
[
  {
    "name": "hello_skill",
    "version": "1.0",
    "enabled": true,
    "skills": ["greet", "add_numbers"]
  }
]
```

### Load Plugin

Load a plugin from the plugins directory.

**Request:**
```
POST /plugin/load/hello_skill
```

**Response:**
```json
{
  "ok": true
}
```

### Unload Plugin

Unload a currently loaded plugin.

**Request:**
```
POST /plugin/unload/hello_skill
```

**Response:**
```json
{
  "ok": true
}
```

### Execute Skill

Execute a specific skill from a plugin.

**Request:**
```
POST /plugin/hello_skill/skill/greet
Content-Type: application/json

{
  "name": "Alice"
}
```

**Response:**
```json
{
  "ok": true,
  "result": "Hello Alice! This is from the hello_skill plugin."
}
```

---

## WebSocket

### Connect

Establish a WebSocket connection for real-time updates.

```
ws://localhost:8000/ws
```

### Messages

**Status Request:**
```json
{
  "action": "status"
}
```

**Response:**
```json
{
  "engine": "ollama"
}
```

**Switch Engine:**
```json
{
  "action": "switch",
  "name": "openai"
}
```

**Response:**
```json
{
  "switched": true,
  "engine": "openai"
}
```

**Get Metrics:**
```json
{
  "action": "metrics"
}
```

**Response:**
```json
{
  "cpu_percent": 25.3,
  "memory_percent": 45.8
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "owner and key required"
}
```

### 404 Not Found

```json
{
  "detail": "Conversation not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently not implemented. Recommended to add before production deployment.

## CORS

All endpoints support CORS (Cross-Origin Resource Sharing).

---

**Last Updated**: January 2026  
**API Version**: 1.0.0
