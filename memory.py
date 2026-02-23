import sqlite3
from datetime import datetime
from typing import List, Dict

DB = "edu_agent.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            topic TEXT,
            content TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            topic TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_note(topic: str, content: str) -> str:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes(created_at, topic, content) VALUES (?,?,?)",
        (datetime.utcnow().isoformat(), topic.strip(), content.strip())
    )
    conn.commit()
    conn.close()
    return f"Saved note → topic: {topic.strip()}"

def search_notes(query: str, limit: int = 8) -> List[Dict[str, str]]:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT topic, content, created_at
        FROM notes
        WHERE topic LIKE ? OR content LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{query}%", f"%{query}%", limit)
    )
    rows = cur.fetchall()
    conn.close()
    return [{"topic": r[0], "content": r[1], "created_at": r[2]} for r in rows]