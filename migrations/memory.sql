-- ===============================
-- MEMORY SYSTEM (SQLite)
-- ===============================

PRAGMA foreign_keys = ON;

-- -------------------------------
-- USER MEMORY
-- -------------------------------
CREATE TABLE IF NOT EXISTS user_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    importance REAL NOT NULL DEFAULT 0.5,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_memory_user
ON user_memory(user_id);

-- -------------------------------
-- SERVER MEMORY
-- -------------------------------
CREATE TABLE IF NOT EXISTS server_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id TEXT NOT NULL,
    content TEXT NOT NULL,
    importance REAL NOT NULL DEFAULT 0.5,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_server_memory_server
ON server_memory(server_id);

-- -------------------------------
-- EMOTIONAL MEMORY
-- -------------------------------
CREATE TABLE IF NOT EXISTS emotional_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    emotion TEXT NOT NULL,
    intensity REAL NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_emotional_memory_user
ON emotional_memory(user_id);

-- -------------------------------
-- EPHEMERAL MEMORY
-- -------------------------------
CREATE TABLE IF NOT EXISTS ephemeral_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope TEXT NOT NULL,
    content TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ephemeral_memory_expiry
ON ephemeral_memory(expires_at);
