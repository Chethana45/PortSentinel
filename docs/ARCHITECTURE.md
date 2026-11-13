# PortSentinel architecture

1. `scanner.py` reads local OS socket tables through psutil.
2. `conflict_detector.py` filters listeners by protocol and checks candidate ports.
3. `monitor.py` records snapshots and emits alerts for newly observed listening endpoints.
4. `database.py` persists snapshots and alerts in SQLite.
5. `main.py` exposes the service through FastAPI.
6. `frontend/` polls the API and renders inventory, history, conflicts and alerts.
7. `cli.py` offers terminal access to scan/check/conflict/suggest operations.

The scanner is intentionally local-only. No remote hosts are contacted.
