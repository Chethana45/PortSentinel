from app.conflict_detector import detect_conflict
from app.scanner import port_status

def test_port_status_detects_listening_owner():
    rows = [{"port": 8080, "protocol": "tcp", "status": "listening", "pid": 42}]
    assert port_status(8080, rows)["in_use"] is True

def test_conflict_detects_matching_protocol(monkeypatch):
    rows = [{"port": 3000, "protocol": "tcp", "status": "listening", "pid": 7}]
    monkeypatch.setattr("app.conflict_detector.find_available_port", lambda *a: 3001)
    result = detect_conflict(3000, "tcp", rows)
    assert result["conflict"] is True
    assert result["suggested_port"] == 3001

def test_udp_does_not_conflict_with_tcp_row(monkeypatch):
    rows = [{"port": 3000, "protocol": "tcp", "status": "listening", "pid": 7}]
    result = detect_conflict(3000, "udp", rows)
    assert result["conflict"] is False
