"""Cross-platform local TCP/UDP socket inspection."""
from __future__ import annotations
import socket
from typing import Any
import psutil

TCP_STATES = {
    "LISTEN": "listening",
    "ESTABLISHED": "established",
    "TIME_WAIT": "time_wait",
    "CLOSE_WAIT": "close_wait",
    "SYN_SENT": "connecting",
    "SYN_RECV": "connecting",
    "FIN_WAIT1": "closing",
    "FIN_WAIT2": "closing",
    "CLOSE": "closed",
    "LAST_ACK": "closing",
    "CLOSING": "closing",
    "NONE": "unknown",
}

def _address(addr: Any) -> dict:
    if not addr:
        return {"ip": None, "port": None}
    return {"ip": getattr(addr, "ip", None), "port": getattr(addr, "port", None)}

def scan_sockets(include_connections: bool = True) -> list[dict]:
    """Return local TCP/UDP sockets visible to the current user.

    AccessDenied entries are skipped safely. This inspects the local machine only;
    it does not scan remote hosts or send network probes.
    """
    records = []
    try:
        connections = psutil.net_connections(kind="inet")
    except (psutil.AccessDenied, OSError):
        connections = []
    for conn in connections:
        if not include_connections and conn.status != psutil.CONN_LISTEN:
            continue
        laddr = _address(conn.laddr)
        if laddr["port"] is None:
            continue
        proto = "tcp" if conn.type == socket.SOCK_STREAM else "udp"
        try:
            process = psutil.Process(conn.pid) if conn.pid else None
            pname = process.name() if process else None
            exe = process.exe() if process else None
            username = process.username() if process else None
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pname, exe, username = None, None, None
        status = TCP_STATES.get(conn.status, conn.status.lower() or "unknown")
        records.append({
            "protocol": proto,
            "local_ip": laddr["ip"],
            "port": laddr["port"],
            "status": status,
            "pid": conn.pid,
            "process_name": pname,
            "executable": exe,
            "username": username,
            "remote_ip": _address(conn.raddr)["ip"] if conn.raddr else None,
            "remote_port": _address(conn.raddr)["port"] if conn.raddr else None,
        })
    # Stable, de-duplicated view: the OS can expose multiple socket rows for one bind.
    unique = {}
    for row in records:
        key = (row["protocol"], row["local_ip"], row["port"], row["pid"], row["status"])
        unique[key] = row
    return sorted(unique.values(), key=lambda r: (r["port"], r["protocol"], r["status"]))

def port_status(port: int, sockets: list[dict] | None = None) -> dict:
    rows = sockets if sockets is not None else scan_sockets()
    matches = [r for r in rows if r["port"] == port and r["status"] in ("listening", "unknown")]
    return {"port": port, "in_use": bool(matches), "owners": matches}

def find_available_port(start: int = 8000, end: int = 9000, protocol: str = "tcp") -> int | None:
    if not (1 <= start <= end <= 65535):
        raise ValueError("Ports must satisfy 1 <= start <= end <= 65535")
    used = {r["port"] for r in scan_sockets() if r["protocol"] == protocol and r["status"] in ("listening", "unknown")}
    for port in range(start, end + 1):
        if port not in used:
            return port
    return None
