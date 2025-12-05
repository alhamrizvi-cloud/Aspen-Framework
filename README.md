# Aspen-Framework

**Automated Reconnaissance Framework for ethical security testing.**

Aspen is designed to help security researchers and pentesters perform reconnaissance efficiently. It includes tools for subdomain enumeration, port scanning, technology fingerprinting, screenshotting, and basic vulnerability mapping. **Use only for authorized testing. Misuse is illegal.**

---

## Features

- **Subdomain Enumeration**: DNS brute-force, wordlists, and API fallback.
- **Port Scanning**: Top ports or full scan, with service detection.
- **Screenshotting**: Headless browser screenshots of discovered hosts.
- **Technology Fingerprinting**: Detect server type, language, CMS, and security headers.
- **Vulnerability Mapping**: Identify missing headers, directory listing, and other basic security issues.
- **Full Scan**: Run all modules automatically for a domain.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/Aspen-Framework.git
cd Aspen-Framework
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scrippip install -r requirements.txt
ts\activate     # Windows
python3 aspen.py <command> --domain <target-domain> [options]

