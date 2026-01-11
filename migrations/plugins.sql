-- ===============================
-- PLUGIN SYSTEM (SQLite)
-- ===============================

PRAGMA foreign_keys = ON;

-- -------------------------------
-- INSTALLED PLUGINS
-- -------------------------------
CREATE TABLE IF NOT EXISTS plugins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    version TEXT,
    enabled INTEGER NOT NULL DEFAULT 1,
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------
-- PLUGIN STATE (PERSISTENT)
-- -------------------------------
CREATE TABLE IF NOT EXISTS plugin_state (
    plugin_name TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (plugin_name, key),
    FOREIGN KEY (plugin_name) REFERENCES plugins(name)
);
