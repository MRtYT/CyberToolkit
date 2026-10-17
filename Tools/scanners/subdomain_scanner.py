"""HTTP-based subdomain discovery."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests


def normalize_domain(domain: str) -> str:
    value = domain.strip().lower().rstrip(".")
    if "://" in value:
        value = urlparse(value).hostname or ""
    if not value or any(char.isspace() for char in value) or "/" in value:
        raise ValueError("enter a valid domain name")
    return value


def check_subdomain(
    domain: str, subdomain: str, timeout: float = 3.0, verify_tls: bool = True
) -> dict[str, object] | None:
    label = subdomain.strip().strip(".")
    if not label:
        return None
    hostname = f"{label}.{domain}"
    for scheme in ("https", "http"):
        try:
            response = requests.get(
                f"{scheme}://{hostname}",
                timeout=timeout,
                allow_redirects=True,
                stream=True,
                verify=verify_tls,
            )
            try:
                return {
                    "subdomain": hostname,
                    "url": response.url,
                    "scheme": scheme,
                    "status": "FOUND",
                    "status_code": response.status_code,
                    "resolved": True,
                }
            finally:
                response.close()
        except requests.RequestException:
            continue
    return None


def scan_subdomains(
    domain: str,
    subdomain_list: list[str],
    threads: int = 40,
    timeout: float = 3.0,
    verify_tls: bool = True,
) -> list[dict[str, object]]:
    if threads < 1 or threads > 200:
        raise ValueError("threads must be between 1 and 200")
    domain = normalize_domain(domain)
    words = list(dict.fromkeys(word.strip() for word in subdomain_list if word.strip()))
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(
            lambda word: check_subdomain(domain, word, timeout, verify_tls), words
        )
        return [result for result in results if result is not None]
