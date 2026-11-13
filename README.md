# 🔍 PortSentinel
### Intelligent Port Conflict Detection & Monitoring

PortSentinel is a cross-platform local port intelligence tool for developers. It inspects TCP/UDP sockets, identifies the processes associated with listening ports, detects conflicts, suggests alternative ports, and records monitoring snapshots.

> **Scope:** PortSentinel inspects the local machine only. It does not perform remote network scans.

---

## ✨ Features

✓ **Phase 1 — Port Scanner**
- List local TCP/UDP sockets.
- Display socket state and local address.
- Identify process IDs (PID).
- Retrieve process names and executable paths where permissions allow.

✓ **Phase 2 — Conflict Detector**
- Check whether a requested TCP/UDP port is occupied.
- Identify processes using a port.
- Detect port conflicts.
- Suggest nearby available alternative ports.

✓ **Phase 3 — Monitoring**
- Capture port activity snapshots.
- Compare listener sets between snapshots.
- Detect newly observed listening ports.
- Generate alerts for new port activity.

✓ **Phase 4 — Web Dashboard**
- Interactive React dashboard.
- Local socket inventory.
- Port search and filtering.
- Quick conflict checks.
- Port activity visualization.
- Alerts interface.

✓ **Phase 5 — History and Safety**
- SQLite snapshot history.
- Alert history and acknowledgement.
- Process inspection API.
- Guarded process termination.
- Explicit termination confirmation.
- PID, process name and owner revalidation.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| FastAPI | Backend API |
| psutil | System and process inspection |
| SQLite | Snapshot and alert storage |
| React | Frontend interface |
| Vite | Frontend development server |
| Tailwind CSS | UI styling |
| Recharts | Data visualization |
| Pytest | Automated testing |

---

## 📁 Project Structure

```text
PortSentinel/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── scanner.py
│   │   ├── process_inspector.py
│   │   ├── conflict_detector.py
│   │   ├── monitor.py
│   │   ├── database.py
│   │   └── cli.py
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── docs/
├── README.md
└── .gitignore
```

---

## ⚙️ Requirements

✓ Python 3.10 or later  
✓ Node.js 18 or later  
✓ npm  
✓ Git

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Chethana45/PortSentinel.git
cd PortSentinel
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / WSL**

```bash
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

✓ Backend runs at:

`http://127.0.0.1:8000`

✓ Interactive API documentation:

`http://127.0.0.1:8000/docs`

---

## 💻 Running the CLI

From the `backend` directory, execute the following commands.

**Scan all local sockets**

```bash
python -m app.cli scan
```

**Display listening sockets**

```bash
python -m app.cli scan --listening
```

**Check a port**

```bash
python -m app.cli check 3000
```

**Detect a TCP port conflict**

```bash
python -m app.cli conflict 3000 --protocol tcp
```

**Suggest an available port**

```bash
python -m app.cli suggest --start 8000 --end 9000
```

✓ Local socket scanning  
✓ Port availability checking  
✓ Conflict detection  
✓ Alternative port suggestions  

---

## 🌐 Running the Frontend Dashboard

Open a second terminal.

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal. Normally:

`http://localhost:5173`

✓ Interactive dashboard  
✓ Socket inventory  
✓ Port search and filtering  
✓ Conflict checking  
✓ Activity visualization  
✓ Alerts interface  

The dashboard expects the backend API at:

`http://127.0.0.1:8000`

Set `VITE_API_URL` if the API runs elsewhere.

---

## 🔌 API Endpoints

| Status | Method | Endpoint | Description |
|---|---|---|---|
| ✓ | GET | `/api/health` | API health |
| ✓ | GET | `/api/ports` | Retrieve current local sockets |
| ✓ | GET | `/api/ports/{port}` | Check port status |
| ✓ | GET | `/api/conflicts/{port}?protocol=tcp` | Detect port conflicts |
| ✓ | GET | `/api/suggest?start=8000&end=9000` | Suggest an available port |
| ✓ | GET | `/api/processes/{pid}` | Inspect a process |
| ✓ | POST | `/api/processes/terminate` | Guarded process termination |
| ✓ | POST | `/api/monitor/snapshot` | Capture a monitoring snapshot |
| ✓ | GET | `/api/history` | Retrieve snapshot history |
| ✓ | GET | `/api/alerts` | Retrieve monitoring alerts |
| ✓ | POST | `/api/alerts/{id}/acknowledge` | Acknowledge an alert |

---

## 🧪 Running Tests

Navigate to the backend directory:

```bash
cd backend
```

Run the test suite:

```bash
pytest -q
```

✓ Automated test execution  
✓ Scanner testing  
✓ Conflict detection testing  
✓ Monitoring testing  

---

## 🔐 Platform and Permission Notes

✓ **Local inspection:** PortSentinel inspects sockets on the local machine only.

✓ **Process permissions:** Process metadata may be unavailable when the current user lacks sufficient permissions. Use elevated privileges only when necessary.

✓ **Windows support:** Run the backend with native Windows Python to inspect Windows host sockets.

✓ **WSL support:** A backend running inside WSL sees the WSL/Linux environment and does not provide a complete view of Windows host processes.

✓ **UDP handling:** UDP sockets do not have a TCP-style `LISTEN` state. They are reported using the socket information provided by the operating system.

✓ **Point-in-time checks:** Port availability can change immediately after a check because another process may claim the port.

✓ **Safe process management:** Process termination requires `confirm: true`, verifies that the PID still maps to the expected process name and current user, and refuses protected PIDs and the API process itself.

---

## 📈 Development Roadmap

| Phase | Implementation | Status |
|---|---|---|
| Phase 1 | Local TCP/UDP Socket Scanner | ✓ Completed |
| Phase 2 | Port Conflict Detection and Alternative Suggestions | ✓ Completed |
| Phase 3 | Snapshot Monitoring and New-Listener Alerts | ✓ Completed |
| Phase 4 | React Web Dashboard | ✓ Completed |
| Phase 5 | SQLite History, Alert Acknowledgement and Guarded Process Management | ✓ Completed |

---

## 🔮 Future Enhancements

- ✓ Advanced port activity analytics
- ✓ Configurable monitoring intervals
- ✓ Exportable monitoring reports
- ✓ Enhanced alert filtering
- ✓ Extended process metadata
- ✓ Improved cross-platform support

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

# 🔍 PortSentinel

**Monitor. Detect. Protect.**

Built with ❤️ for developers.

</div>
