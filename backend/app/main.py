from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .scanner import scan_sockets, port_status, find_available_port
from .conflict_detector import detect_conflict
from .process_inspector import inspect_process, terminate_process
from .monitor import take_snapshot
from . import database

app = FastAPI(title="PortSentinel API", version="1.0.0",
              description="Local port inspection, conflict detection and monitoring.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    database.init_db()

class TerminateRequest(BaseModel):
    pid: int = Field(gt=1)
    expected_name: str
    confirm: bool = False

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "PortSentinel"}

@app.get("/api/ports")
def ports(listening_only: bool = False):
    try:
        rows = scan_sockets(include_connections=not listening_only)
        return {"count": len(rows), "sockets": rows}
    except Exception as exc:
        raise HTTPException(500, str(exc))

@app.get("/api/ports/{port}")
def check_port(port: int):
    if not 1 <= port <= 65535:
        raise HTTPException(400, "Port must be between 1 and 65535")
    return port_status(port)

@app.get("/api/conflicts/{port}")
def conflict(port: int, protocol: str = "tcp"):
    if not 1 <= port <= 65535 or protocol not in ("tcp", "udp"):
        raise HTTPException(400, "Use a valid port and tcp/udp protocol")
    return detect_conflict(port, protocol)

@app.get("/api/suggest")
def suggest(start: int = 8000, end: int = 9000, protocol: str = "tcp"):
    if protocol not in ("tcp", "udp"):
        raise HTTPException(400, "Protocol must be tcp or udp")
    try:
        return {"protocol": protocol, "port": find_available_port(start, end, protocol)}
    except ValueError as exc:
        raise HTTPException(400, str(exc))

@app.get("/api/processes/{pid}")
def process(pid: int):
    try:
        return inspect_process(pid)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(404 if isinstance(exc, ValueError) else 403, str(exc))

@app.post("/api/processes/terminate")
def terminate(req: TerminateRequest):
    try:
        return terminate_process(req.pid, req.expected_name, req.confirm)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    except PermissionError as exc:
        raise HTTPException(403, str(exc))

@app.post("/api/monitor/snapshot")
def snapshot():
    return take_snapshot()

@app.get("/api/history")
def get_history(limit: int = 50):
    return {"history": database.history(max(1, min(limit, 500)))}

@app.get("/api/alerts")
def alerts(limit: int = 100):
    return {"alerts": database.list_alerts(max(1, min(limit, 500)))}

@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge(alert_id: int):
    if not database.acknowledge_alert(alert_id):
        raise HTTPException(404, "Alert not found")
    return {"acknowledged": True, "id": alert_id}
