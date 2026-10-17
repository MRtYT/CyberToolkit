"""CyberToolkit command-line interface."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from tools.dns_lookup import lookup
from tools.hash_tool import SUPPORTED_ALGORITHMS, hash_file, hash_text
from tools.http_inspector import inspect_url
from tools.network_info import get_network_info
from tools.scanners.port_scanner import scan_ports, validate_port_range
from tools.scanners.subdomain_scanner import scan_subdomains

DEFAULT_SUBDOMAINS = [
    "www", "mail", "ftp", "admin", "blog", "dev", "test", "api",
    "staging", "vpn", "support", "autodiscover",
]


def clear_screen() -> None:
    """Clear the terminal before displaying a fresh interactive menu."""
    os.system("cls" if sys.platform == "win32" else "clear")


def read_wordlist(path: str) -> list[str]:
    try:
        with Path(path).open(encoding="utf-8") as file:
            return [
                line.strip()
                for line in file
                if line.strip() and not line.lstrip().startswith("#")
            ]
    except OSError as exc:
        raise ValueError(f"could not read wordlist: {exc}") from exc


def print_result(result: object, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    elif isinstance(result, list):
        for item in result:
            print_result(item)
    else:
        print(result)


def run_ports(args: argparse.Namespace) -> list[dict[str, object]]:
    validate_port_range(args.start, args.end)
    return scan_ports(
        args.target,
        range(args.start, args.end + 1),
        threads=args.threads,
        timeout=args.timeout,
    )


def run_subdomains(args: argparse.Namespace) -> list[dict[str, object]]:
    words = read_wordlist(args.wordlist) if args.wordlist else DEFAULT_SUBDOMAINS
    return scan_subdomains(
        args.domain,
        words,
        threads=args.threads,
        timeout=args.timeout,
        verify_tls=not args.insecure,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CyberToolkit: educational tools for authorized testing."
    )
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    subparsers = parser.add_subparsers(dest="command")

    ports = subparsers.add_parser("ports", help="scan TCP ports")
    ports.add_argument("target")
    ports.add_argument("--start", type=int, default=1)
    ports.add_argument("--end", type=int, default=1024)
    ports.add_argument("--threads", type=int, default=30)
    ports.add_argument("--timeout", type=float, default=2.0)
    ports.set_defaults(handler=run_ports)

    subdomains = subparsers.add_parser("subdomains", help="discover HTTP subdomains")
    subdomains.add_argument("domain")
    subdomains.add_argument("--wordlist")
    subdomains.add_argument("--threads", type=int, default=40)
    subdomains.add_argument("--timeout", type=float, default=3.0)
    subdomains.add_argument("--insecure", action="store_true")
    subdomains.set_defaults(handler=run_subdomains)

    dns = subparsers.add_parser("dns", help="resolve a hostname")
    dns.add_argument("hostname")
    dns.set_defaults(handler=lambda args: lookup(args.hostname))

    http = subparsers.add_parser("http", help="inspect HTTP security headers")
    http.add_argument("url")
    http.add_argument("--timeout", type=float, default=5.0)
    http.set_defaults(handler=lambda args: inspect_url(args.url, args.timeout))

    hashing = subparsers.add_parser("hash", help="hash text or a file")
    source = hashing.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file")
    hashing.add_argument("--algorithm", choices=sorted(SUPPORTED_ALGORITHMS), default="sha256")
    hashing.set_defaults(
        handler=lambda args: {
            "algorithm": args.algorithm,
            "digest": hash_text(args.text, args.algorithm)
            if args.text is not None
            else hash_file(args.file, args.algorithm),
        }
    )

    network = subparsers.add_parser("network-info", help="show local network information")
    network.set_defaults(handler=lambda args: get_network_info())
    return parser


def interactive() -> None:
    while True:
        clear_screen()
        print("\nCyberToolkit")
        print("[1] TCP port scanner")
        print("[2] Subdomain scanner")
        print("[3] DNS lookup")
        print("[4] HTTP security inspector")
        print("[5] Hash text")
        print("[6] Local network info")
        print("[7] Exit")
        choice = input("cyberToolkit > ").strip()
        try:
            if choice == "1":
                target = input("Target: ").strip()
                start = int(input("Start port [1]: ") or "1")
                end = int(input("End port [1024]: ") or "1024")
                print_result(run_ports(argparse.Namespace(
                    target=target, start=start, end=end, threads=30, timeout=2.0
                )))
            elif choice == "2":
                domain = input("Domain: ").strip()
                print_result(run_subdomains(argparse.Namespace(
                    domain=domain, wordlist=None, threads=40, timeout=3.0, insecure=False
                )))
            elif choice == "3":
                print_result(lookup(input("Hostname: ")))
            elif choice == "4":
                print_result(inspect_url(input("URL: ")))
            elif choice == "5":
                print(hash_text(input("Text: ")))
            elif choice == "6":
                print_result(get_network_info())
            elif choice == "7":
                return
            else:
                print("Invalid option.")
        except (ValueError, RuntimeError) as exc:
            print(f"Error: {exc}")
        input("\nPress Enter to continue...")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        interactive()
        return 0
    try:
        result = args.handler(args)
        print_result(result, args.json if hasattr(args, "json") else False)
        return 0
    except (ValueError, RuntimeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    sys.exit(main())
