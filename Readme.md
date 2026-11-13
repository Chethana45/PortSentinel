# 🔍 PortSentinel
### Intelligent Port Conflict Detection & Monitoring System

**PortSentinel** is a cross-platform port monitoring tool designed to help developers identify port conflicts, inspect processes using network ports, and monitor port activity in real time.

Ever encountered the frustrating `Port already in use` error while running your application? PortSentinel helps you understand what's occupying a port, identify the responsible process, and find available alternatives.

---

## ✨ Features

- **Port Scanning** – Identify open, occupied, and available local ports.
- **Process Identification** – Retrieve process IDs (PID), process names, and executable details.
- **Conflict Detection** – Detect port conflicts that may prevent applications from starting.
- **Real-Time Monitoring** – Monitor local port activity continuously.
- **Alternative Port Suggestions** – Find available ports when a requested port is occupied.
- **Cross-Platform Support** – Designed for Windows and Linux.
- **CLI Interface** – Inspect ports directly from the terminal.
- **Web Dashboard** – Visualize port usage and monitoring information.

> Features will be implemented progressively as the project develops.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Process Monitoring | psutil |
| Frontend | React |
| Styling | Tailwind CSS |
| Data Visualization | Recharts |
| Database | SQLite |
| Testing | Pytest |
| Version Control | Git & GitHub |

## 🏗️ Architecture

```text
              ┌──────────────────────┐
              │      User            │
              └──────────┬───────────┘
                         │
               ┌─────────▼─────────┐
               │   CLI / Dashboard │
               └─────────┬─────────┘
                         │
               ┌─────────▼─────────┐
               │    FastAPI        │
               │    Backend        │
               └─────────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
  ┌─────▼─────┐   ┌──────▼──────┐  ┌──────▼──────┐
  │   Port    │   │   Process   │  │  Conflict   │
  │  Scanner  │   │  Inspector  │  │  Detector   │
  └─────┬─────┘   └──────┬──────┘  └──────┬──────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                ┌────────▼────────┐
                │  SQLite Storage │
                └─────────────────┘
```

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
│   │   └── database.py
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
│
├── docs/
│
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Chethana45/PortSentinel.git
cd PortSentinel
```

### 2. Set up the backend

```bash
cd backend

python -m venv venv
```

**Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the backend

```bash
uvicorn app.main:app --reload
```

API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

*These instructions will become runnable as the corresponding components are implemented.*

## 🗺️ Development Roadmap

- [ ] **Phase 1 – Port Scanner**
  - Scan local TCP and UDP ports.
  - Identify occupied and available ports.
  - Retrieve process information.

- [ ] **Phase 2 – Conflict Detection**
  - Detect port conflicts.
  - Identify processes blocking requested ports.
  - Suggest alternative available ports.

- [ ] **Phase 3 – Real-Time Monitoring**
  - Continuously monitor port activity.
  - Track changes in port usage.
  - Maintain port activity history.

- [ ] **Phase 4 – Web Dashboard**
  - Build an interactive dashboard.
  - Display port usage statistics.
  - Visualize occupied and available ports.

- [ ] **Phase 5 – Advanced Capabilities**
  - Configurable monitoring alerts.
  - Port usage analytics.
  - Safe, user-confirmed process management.

## 🔐 Safety & Privacy

- Designed for local system monitoring.
- Does not require sending port information to an external server.
- Process termination, if implemented, will require explicit user confirmation.
- Some process details may require elevated permissions.

## 🎯 Project Goals

PortSentinel aims to simplify local network port management by providing developers with better visibility into their system's port usage.

Instead of manually checking ports through terminal commands, developers can use one tool to inspect, monitor, and troubleshoot port conflicts.

## 🤝 Contributing

Contributions, suggestions, and feature requests are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

## 📜 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with 💻 to make debugging easier.**

⭐ If you find PortSentinel interesting, consider starring the repository!

</div>
