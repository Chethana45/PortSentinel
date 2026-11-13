from .scanner import port_status, find_available_port

def detect_conflict(port: int, protocol: str = "tcp", sockets: list[dict] | None = None) -> dict:
    status = port_status(port, sockets)
    owners = [o for o in status["owners"] if o["protocol"] == protocol]
    alternative = find_available_port(max(1024, port + 1), min(65535, port + 100), protocol) if owners else None
    return {
        "port": port, "protocol": protocol, "conflict": bool(owners),
        "owners": owners, "suggested_port": alternative,
        "message": f"{protocol.upper()} port {port} is occupied" if owners else f"{protocol.upper()} port {port} appears available"
    }
