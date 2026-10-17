"""Inspect HTTP response metadata and common security headers."""

from __future__ import annotations

from urllib.parse import urlparse

import requests

SECURITY_HEADERS = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy",
)


def inspect_url(url: str, timeout: float = 5.0) -> dict[str, object]:
    value = url.strip()
    if not value:
        raise ValueError("URL cannot be empty")
    if "://" not in value:
        value = f"https://{value}"
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL must use http or https and include a hostname")
    try:
        response = requests.get(
            value, timeout=timeout, allow_redirects=True, stream=True
        )
        try:
            headers = {name: response.headers.get(name) for name in SECURITY_HEADERS}
            return {
                "url": response.url,
                "status_code": response.status_code,
                "server": response.headers.get("Server"),
                "content_type": response.headers.get("Content-Type"),
                "security_headers": headers,
                "missing_security_headers": [
                    name for name, header_value in headers.items() if not header_value
                ],
            }
        finally:
            response.close()
    except requests.RequestException as exc:
        raise RuntimeError(f"HTTP request failed: {exc}") from exc
