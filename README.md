# CyberToolkit

CyberToolkit is a learning-focused Python toolkit for **authorized** security
testing and network programming practice. It is not a replacement for Nmap,
Burp Suite, or Wireshark.

## Features

| Command | Purpose |
| --- | --- |
| `ports` | Concurrent TCP scanning with service lookup and banner probing |
| `subdomains` | HTTP/HTTPS subdomain discovery using a wordlist |
| `dns` | Resolve a hostname to IPv4/IPv6 addresses |
| `http` | Inspect status, redirects, and common security headers |
| `hash` | Hash text or files with MD5, SHA-1, SHA-256, or SHA-512 |
| `network-info` | Display the local hostname and address |

The original interactive menu remains available when the program is run
without a command.

## Installation

Python 3.10 or newer is recommended:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

```bash
# Interactive menu
python main.py

# Scan TCP ports
python main.py ports example.com --start 1 --end 1024 --threads 30

# Use a custom wordlist
python main.py subdomains example.com --wordlist Wordlists/common.txt

# Resolve DNS
python main.py dns example.com

# Inspect HTTP security headers
python main.py http https://example.com

# Hash data
python main.py hash --text "hello" --algorithm sha256
python main.py hash --file image.iso --algorithm sha256

# Get local network information
python main.py network-info

# Any command can emit JSON for scripts (place --json before the command)
python main.py --json dns example.com
```

Subdomain wordlists ignore blank lines, comments beginning with `#`, and
duplicate entries. TLS verification is enabled by default; use
`--insecure` only for controlled testing with certificates you understand.

## Development

Run the standard-library test suite:

```bash
python -m unittest discover -s tests -v
```

The scanners intentionally use conservative timeouts and bounded worker
counts. Results distinguish open, closed, and error states where possible.

## Responsible use

Only scan systems, domains, and files that you own or have explicit permission
to test. Respect rate limits, terms of service, privacy requirements, and
applicable laws. The authors are not responsible for unauthorized use.
