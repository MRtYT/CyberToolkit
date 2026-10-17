"""TCP port scanning with optional banner grabbing."""

from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass
class PortResult:
    port: int
    status: str
    service: str
    banner: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def validate_port_range(start: int, end: int) -> None:
    if not 1 <= start <= 65535 or not 1 <= end <= 65535:
        raise ValueError("ports must be between 1 and 65535")
    if start > end:
        raise ValueError("start port must not be greater than end port")


def get_service(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except (OSError, OverflowError):
        return "unknown"


def _clean_banner(data: bytes, http: bool = False) -> str | None:
    if not data:
        return None
    text = data.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    return text.splitlines()[0][:200] if http else text.splitlines()[0][:200]


def check_port(host: str, port: int, timeout: float = 2.0) -> PortResult:
    service = get_service(port)
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            if port in {80, 8000, 8080, 443, 8443}:
                request = (
                    f"HEAD / HTTP/1.1\r\nHost: {host}\r\n"
                    "User-Agent: CyberToolkit/1.0\r\nConnection: close\r\n\r\n"
                )
                sock.sendall(request.encode("ascii"))
            else:
                sock.sendall(b"\r\n")
            try:
                banner = _clean_banner(sock.recv(4096), port in {80, 8000, 8080, 443, 8443})
            except socket.timeout:
                banner = None
            return PortResult(port, "OPEN", service, banner)
    except (ConnectionRefusedError, socket.timeout):
        return PortResult(port, "CLOSED", service)
    except OSError as exc:
        return PortResult(port, "ERROR", service, error=str(exc))


def scan_ports(
    host: str, ports: Iterable[int], threads: int = 30, timeout: float = 2.0
) -> list[dict[str, object]]:
    if threads < 1 or threads > 200:
        raise ValueError("threads must be between 1 and 200")
    port_list = list(ports)
    if not port_list:
        return []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda port: check_port(host, port, timeout), port_list)
        return [result.to_dict() for result in results]
