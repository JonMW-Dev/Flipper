APP_NAME   = "Flipper"
APP_AUTHOR = "JMW"
CONFIG_DEFAULTS = {
    "API_KEY":"",
    "base_url":"localhost",
    "model":"None"
}

DEF_TESTBANK = """
    CREATE TABLE testbank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_valid INTEGER NOT NULL DEFAULT 0,
        course TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        f1 TEXT,
        f2 TEXT,
        f3 TEXT,
        correct INTEGER DEFAULT 0,
        attempts INTEGER DEFAULT 0
    )
"""

DEF_COURSES = """
    CREATE TABLE  courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        course TEXT NOT NULL
    )
"""

DEF_AICHAT_CONFIG = """
    CREATE TABLE ai_chat_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        api_key TEXT,
        url TEXT NOT NULL,
        model TEXT
    )
"""
