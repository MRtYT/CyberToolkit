"""DNS lookup utility using the standard library."""

from __future__ import annotations

import socket


def lookup(hostname: str) -> dict[str, object]:
    hostname = hostname.strip()
    if not hostname:
        raise ValueError("hostname cannot be empty")
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(hostname, None)})
    except socket.gaierror as exc:
        raise ValueError(f"DNS lookup failed: {exc}") from exc
    return {"hostname": hostname, "addresses": addresses}
