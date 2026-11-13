# 🔍 PortSentinel
### Intelligent Port Conflict Detection & Monitoring

PortSentinel is a cross-platform local port intelligence tool for developers. It inspects TCP/UDP sockets, identifies the processes associated with listening ports, detects conflicts, suggests alternative ports, and records monitoring snapshots.

> **Scope:** PortSentinel inspects the local machine only. It does not perform remote network scans.

## Features

- **Phase 1 — Port scanner:** list local TCP/UDP sockets, state, local address, PID, process name and executable where permissions allow.
- **Phase 2 — Conflict detector:** check a requested TCP/UDP port and suggest a nearby available alternative.
- **Phase 3 — Monitoring:** capture snapshots, compare listener sets and create alerts for newly observed listening ports.
- **Phase 4 — Web dashboard:** React dashboard with socket inventory, search, conflict checks, activity chart and alerts.
- **Phase 5 — History and safety:** SQLite snapshot/alert history, alert acknowledgement, process inspection API, and guarded process termination requiring explicit confirmation and PID/name/owner revalidation.

## Tech stack

Python · FastAPI · psutil · SQLite · React · Vite · Tailwind CSS · Recharts · Pytest

## Project structure

```text
PortSentinel/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── scanner.py
│   │   ├── process_inspector.py
│   │   ├── conflict_detector.py
│   │   ├── monitor.py
│   │   ├── database.py
│   │   └── cli.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
├── docs/
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10+
- Node.js 18+
- npm

## Run the backend

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / WSL**
```bash
source .venv/bin/activate
```

Install and start:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Run the CLI

From the `backend` directory:

```bash
python -m app.cli scan
python -m app.cli scan --listening
python -m app.cli check 3000
python -m app.cli conflict 3000 --protocol tcp
python -m app.cli suggest --start 8000 --end 9000
```

## Run the dashboard

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (normally http://localhost:5173).

The dashboard expects the API at `http://127.0.0.1:8000`. Set `VITE_API_URL` if your API runs elsewhere.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | API health |
| GET | `/api/ports` | Current local sockets |
| GET | `/api/ports/{port}` | Check port status |
| GET | `/api/conflicts/{port}?protocol=tcp` | Detect a conflict |
| GET | `/api/suggest?start=8000&end=9000` | Suggest a free port |
| GET | `/api/processes/{pid}` | Inspect a process |
| POST | `/api/processes/terminate` | Explicitly confirmed process termination |
| POST | `/api/monitor/snapshot` | Capture a snapshot and detect new listeners |
| GET | `/api/history` | Snapshot history |
| GET | `/api/alerts` | Monitoring alerts |
| POST | `/api/alerts/{id}/acknowledge` | Acknowledge an alert |

## Run tests

```bash
cd backend
pytest -q
```

## Platform and permission notes

- Process metadata can be unavailable when the current user lacks permission. Run with appropriate privileges only when necessary.
- On Windows, run the backend with native Windows Python to inspect Windows host sockets. A backend inside WSL sees the WSL/Linux environment and does not provide a complete view of Windows host processes.
- UDP sockets do not have a TCP-style `LISTEN` state; they are reported using the OS socket information available.
- A port check is a point-in-time observation. Another process can claim a port immediately after the check.
- The process termination endpoint is intentionally guarded. It requires `confirm: true`, verifies the PID still maps to the expected process name and current user, and refuses protected PIDs and the API process itself. Use process termination carefully.

## Development roadmap

- [x] Phase 1 — Local TCP/UDP socket scanner
- [x] Phase 2 — Port conflict detection and alternative suggestions
- [x] Phase 3 — Snapshot monitoring and new-listener alerts
- [x] Phase 4 — React web dashboard
- [x] Phase 5 — SQLite history, alert acknowledgement and guarded process management

## License

MIT
