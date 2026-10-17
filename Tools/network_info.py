"""Safe local network information helpers."""

from __future__ import annotations

import socket


def get_network_info() -> dict[str, str]:
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        local_ip = "unavailable"
    return {"hostname": hostname, "local_ip": local_ip}
