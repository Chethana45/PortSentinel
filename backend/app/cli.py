"""PortSentinel command-line interface."""
import argparse, json
from .scanner import scan_sockets, port_status, find_available_port
from .conflict_detector import detect_conflict

def main():
    parser = argparse.ArgumentParser(prog="portsentinel", description="Inspect local machine ports.")
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan", help="List local sockets")
    scan.add_argument("--listening", action="store_true")
    check = sub.add_parser("check", help="Check a port")
    check.add_argument("port", type=int)
    conflict = sub.add_parser("conflict", help="Check a TCP/UDP port conflict")
    conflict.add_argument("port", type=int)
    conflict.add_argument("--protocol", choices=["tcp", "udp"], default="tcp")
    suggest = sub.add_parser("suggest", help="Find an available port")
    suggest.add_argument("--start", type=int, default=8000)
    suggest.add_argument("--end", type=int, default=9000)
    suggest.add_argument("--protocol", choices=["tcp", "udp"], default="tcp")
    args = parser.parse_args()
    if args.command == "scan":
        result = {"sockets": scan_sockets(not args.listening)}
    elif args.command == "check":
        result = port_status(args.port)
    elif args.command == "conflict":
        result = detect_conflict(args.port, args.protocol)
    else:
        result = {"port": find_available_port(args.start, args.end, args.protocol)}
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
