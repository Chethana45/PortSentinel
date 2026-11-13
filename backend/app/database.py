import os, sqlite3, json, time
from pathlib import Path

DB_PATH = Path(os.getenv("PORTSENTINEL_DB", Path(__file__).resolve().parents[1] / "portsentinel.db"))

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT, captured_at REAL NOT NULL,
            socket_count INTEGER NOT NULL, listening_count INTEGER NOT NULL,
            payload TEXT NOT NULL)""")
        db.execute("""CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at REAL NOT NULL,
            severity TEXT NOT NULL, title TEXT NOT NULL, details TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0)""")

def save_snapshot(sockets):
    now = time.time()
    listening = [s for s in sockets if s["status"] == "listening"]
    with connect() as db:
        db.execute("INSERT INTO snapshots(captured_at,socket_count,listening_count,payload) VALUES(?,?,?,?)",
                   (now, len(sockets), len(listening), json.dumps(sockets)))
    return {"captured_at": now, "socket_count": len(sockets), "listening_count": len(listening)}

def history(limit=50):
    with connect() as db:
        rows = db.execute("SELECT id,captured_at,socket_count,listening_count FROM snapshots ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in reversed(rows)]

def create_alert(severity, title, details):
    with connect() as db:
        cur = db.execute("INSERT INTO alerts(created_at,severity,title,details) VALUES(?,?,?,?)",
                         (time.time(), severity, title, details))
        return cur.lastrowid

def list_alerts(limit=100):
    with connect() as db:
        rows = db.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]

def acknowledge_alert(alert_id):
    with connect() as db:
        cur = db.execute("UPDATE alerts SET acknowledged=1 WHERE id=?", (alert_id,))
        return cur.rowcount > 0
