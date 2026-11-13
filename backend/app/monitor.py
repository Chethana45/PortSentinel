"""Polling monitor with SQLite history and newly-observed listening-port alerts."""
from .scanner import scan_sockets
from .database import save_snapshot, create_alert

_previous = set()

def take_snapshot():
    global _previous
    sockets = scan_sockets()
    summary = save_snapshot(sockets)
    current = {(s["protocol"], s["local_ip"], s["port"], s["pid"])
               for s in sockets if s["status"] == "listening"}
    for item in sorted(current - _previous):
        proto, ip, port, pid = item
        create_alert("info", f"New listening port: {port}/{proto}",
                     f"{ip or '*'}:{port} is now listening (PID: {pid or 'unknown'}).")
    _previous = current
    return {"summary": summary, "sockets": sockets}
