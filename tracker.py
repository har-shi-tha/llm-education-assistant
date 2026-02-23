import sqlite3
from datetime import datetime
from typing import List, Dict
from memory import DB

VALID = {"todo", "doing", "done"}

def set_status(topic: str, status: str) -> str:
    status = status.lower().strip()
    if status not in VALID:
        return "Status must be one of: todo, doing, done"

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO progress(created_at, topic, status) VALUES (?,?,?)",
        (datetime.utcnow().isoformat(), topic.strip(), status)
    )
    conn.commit()
    conn.close()
    return f"Updated progress → {topic.strip()} = {status}"

def get_latest_progress(limit: int = 30) -> List[Dict[str, str]]:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT topic, status, created_at
        FROM progress
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return [{"topic": r[0], "status": r[1], "created_at": r[2]} for r in rows]