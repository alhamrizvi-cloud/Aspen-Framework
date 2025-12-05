#!/usr/bin/env python3
"""
Aspen - Automated Reconnaissance Framework
Created by Alham Rizvi

This tool is for ethical reconnaissance only. Use responsibly and with permission.
"""

import argparse
import os
import sys
import json
import time
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from pathlib import Path

# External libraries (install as per instructions)
import requests
from scapy.all import sr1, IP, TCP, UDP, ICMP  # For port scanning (requires root on some systems)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Constants
RESULTS_DIR = "results"
SCREENSHOTS_DIR = "screenshots"
LOGS_DIR = "logs"
DEFAULT_WORDLIST = "wordlists/subdomains.txt"  # Provide your own wordlist
DEFAULT_THREADS = 10
TIMEOUT = 5

# Create directories
for dir_name in [RESULTS_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
    Path(dir_name).mkdir(exist_ok=True)

# Rich console for output
console = Console()

class AspenFramework:
    def __init__(self, args):
        self.args = args
        self.console = console
        self.progress = Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True)

    def log(self, message, level="info"):
        """Log messages with colors."""
        if self.args.silent:
            return
        if level == "error":
            self.console.print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
        elif level == "success":
            self.console.print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")
        elif level == "warning":
            self.console.print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")
        else:
            if self.args.verbose:
                self.console.print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {message}")

    def save_results(self, data, filename, json_format=False):
        """Save results to file."""
        if not self.args.save:
            return
        filepath = os.path.join(RESULTS_DIR, filename)
        with open(filepath, 'w') as f:
            if json_format:
                json.dump(data, f, indent=4)
            else:
                f.write(data)
        self.log(f"Results saved to {filepath}", "success")

    # 1. Subdomain Enumeration
    def enumerate_subdomains(self, domain):
        """Enumerate subdomains using brute-force, wordlist, and API fallback."""
        self.log("Starting subdomain enumeration...")
        subdomains = set()
        threads = self.args.threads or DEFAULT_THREADS

        # Brute-force (simple DNS queries)
        def check_subdomain(sub):
            try:
                import dns.resolver
                answers = dns.resolver.resolve(f"{sub}.{domain}", 'A')
                for rdata in answers:
                    subdomains.add(f"{sub}.{domain}")
            except:
                pass

        # Wordlist-based
        wordlist = self.args.wordlist or DEFAULT_WORDLIST
        if os.path.exists(wordlist):
            with open(wordlist, 'r') as f:
                subs = [line.strip() for line in f if line.strip()]
            with self.progress as progress:
                task = progress.add_task("Enumerating subdomains...", total=len(subs))
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = [executor.submit(check_subdomain, sub) for sub in subs]
                    for future in as_completed(futures):
                        progress.update(task, advance=1)

        # API fallback (e.g., crt.sh)
        try:
            response = requests.get(f"https://crt.sh/?q={domain}&output=json", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    sub = entry['name_value'].lower()
                    if sub.endswith(f".{domain}"):
                        subdomains.add(sub)
        except:
            self.log("API fallback failed", "warning")

        result = "\n".join(sorted(subdomains))
        self.save_results(result, f"subdomains_{domain}.txt")
        return subdomains

    # 2. Port Scanning
    def scan_ports(self, target):
        """Scan ports with service detection."""
        self.log("Starting port scan...")
        open_ports = {}
        ports = list(range(1, 1025)) if self.args.top_ports else list(range(0, 65536))  # Top 1024 or full

        def scan_port(port):
            try:
                pkt = IP(dst=target)/TCP(dport=port, flags="S")
                resp = sr1(pkt, timeout=TIMEOUT, verbose=0)
                if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:  # SYN-ACK
                    # Banner grabbing (simple)
                    service = "unknown"
                    try:
                        banner = sr1(IP(dst=target)/TCP(dport=port, flags="A"), timeout=1, verbose=0)
                        if banner and banner.haslayer(TCP):
                            service = "detected"  # Placeholder; enhance with nmap-like logic
                    except:
                        pass
                    open_ports[port] = service
            except:
                pass

        with self.progress as progress:
            task = progress.add_task("Scanning ports...", total=len(ports))
            with ThreadPoolExecutor(max_workers=self.args.threads or DEFAULT_THREADS) as executor:
                futures = [executor.submit(scan_port, port) for port in ports]
                for future in as_completed(futures):
                    progress.update(task, advance=1)

        # Output as table
        table = Table(title="Open Ports")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="magenta")
        for port, service in open_ports.items():
            table.add_row(str(port), service)
        self.console.print(table)

        # JSON output
        self.save_results(open_ports, f"ports_{target}.json", json_format=True)
        return open_ports

    # 3. Screenshotting
    def take_screenshot(self, url):
        """Take screenshot of URL using Selenium."""
        self.log("Taking screenshot...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)  # Ensure chromedriver is installed
        try:
            driver.get(url)
            time.sleep(2)  # Wait for load
            filename = f"{urlparse(url).netloc}.png"
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            driver.save_screenshot(filepath)
            self.log(f"Screenshot saved to {filepath}", "success")
        except Exception as e:
            self.log(f"Screenshot failed: {e}", "error")
        finally:
            driver.quit()

    # 4. Technology Fingerprinting
    def fingerprint_tech(self, url):
        """Detect tech stack."""
        self.log("Fingerprinting technology...")
        try:
            response = requests.get(url, timeout=TIMEOUT)
            headers = response.headers
            tech = {
                "server": headers.get("Server", "unknown"),
                "language": "unknown",  # Heuristic: check for common frameworks
                "cms": "unknown",
                "security_headers": {}
            }
            # Basic heuristics
            if "X-Powered-By" in headers:
                tech["language"] = headers["X-Powered-By"]
            if "WordPress" in response.text:
                tech["cms"] = "WordPress"
            # Security headers
            sec_headers = ["X-Frame-Options", "Content-Security-Policy", "X-Content-Type-Options"]
            for h in sec_headers:
                tech["security_headers"][h] = h in headers
            self.save_results(tech, f"tech_{urlparse(url).netloc}.json", json_format=True)
            return tech
        except Exception as e:
            self.log(f"Fingerprinting failed: {e}", "error")
            return {}

    # 5. Vulnerability Mapping
    def map_vulns(self, url):
        """Basic vulnerability checks."""
        self.log("Mapping vulnerabilities...")
        vulns = []
        try:
            response = requests.get(url, timeout=TIMEOUT)
            # Checks
            if "Index of /" in response.text:
                vulns.append("Directory listing enabled")
            if response.status_code == 200 and "default" in response.text.lower():
                vulns.append("Default page detected")
            headers = response.headers
            missing_headers = []
            for h in ["X-Frame-Options", "X-Content-Type-Options"]:
                if h not in headers:
                    missing_headers.append(h)
            if missing_headers:
                vulns.append(f"Missing security headers: {', '.join(missing_headers)}")
            if "Server" in headers and "old" in headers["Server"].lower():  # Placeholder
                vulns.append("Outdated server version")
            report = "\n".join(vulns) if vulns else "No basic vulnerabilities detected"
            self.save_results(report, f"vulns_{urlparse(url).netloc}.txt")
            return report
        except Exception as e:
            self.log(f"Vuln mapping failed: {e}", "error")
            return "Error in vuln mapping"

    def full_scan(self, domain):
        """Run all modules."""
        self.log("Starting full scan...")
        url = f"https://{domain}"
        subdomains = self.enumerate_subdomains(domain)
        # Assume IP from domain for scanning (simplified)
        import socket
        try:
            target_ip = socket.gethostbyname(domain)
            ports = self.scan_ports(target_ip)
        except:
            self.log("Port scan skipped (DNS resolution failed)", "warning")
        self.take_screenshot(url)
        tech = self.fingerprint_tech(url)
        vulns = self.map_vulns(url)
        self.log("Full scan complete", "success")

def main():
    # 3D ASCII Art Banner (simplified; use a tool like figlet for full 3D)
    banner = """
    █████╗ ███████╗██████╗ ███████╗███╗   ██╗
    ██╔══██╗██╔════╝██╔══██╗██╔════╝████╗  ██║
    ███████║███████╗██████╔╝█████╗  ██╔██╗ ██║
    ██╔══██║╚════██║██╔═══╝ ██╔══╝  ██║╚██╗██║
    ██║  ██║███████║██║     ███████╗██║ ╚████║
    ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝
    Automated Recon Framework
    Created by Alham Rizvi
    """
    console.print(Panel(banner, title="Aspen", border_style="bold blue"))

    # Description Header
    description = """
    Aspen is an Automated Reconnaissance Framework for ethical security testing.
    It performs subdomain enumeration, port scanning, screenshotting, technology fingerprinting, and basic vulnerability mapping.
    Use only for authorized reconnaissance. Misuse is illegal.
    Features:
    - Subdomain Enumeration (DNS brute-force, wordlists, API fallback)
    - Port Scanning (top/full, with service detection)
    - Screenshotting (headless browser)
    - Technology Fingerprinting (server, language, CMS, security headers)
    - Vulnerability Mapping (missing headers, directory listing, etc.)
    """
    console.print(Panel(description, title="About Aspen", border_style="green"))

    parser = argparse.ArgumentParser(description="Aspen - Automated Recon Framework")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommands
    enum_parser = subparsers.add_parser("enum", help="Enumerate subdomains")
    enum_parser.add_argument("--domain", required=True, help="Target domain")

    scan_parser = subparsers.add_parser("scan", help="Scan ports")
    scan_parser.add_argument("--target", required=True, help="Target IP")

    tech_parser = subparsers.add_parser("tech", help="Fingerprint technology")
    tech_parser.add_argument("--url", required=True, help="Target URL")

    screenshot_parser = subparsers.add_parser("screenshot", help="Take screenshot")
    screenshot_parser.add_argument("--url", required=True, help="Target URL")

    vulns_parser = subparsers.add_parser("vulns", help="Map vulnerabilities")
    vulns_parser.add_argument("--url", required=True, help="Target URL")

    fullscan_parser = subparsers.add_parser("fullscan", help="Run full scan")
    fullscan_parser.add_argument("--domain", required=True, help="Target domain")

    # Global options
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--json", action="store_true", help="Output in JSON")
    parser.add_argument("--threads", type=int, help="Number of threads")
    parser.add_argument("--silent", action="store_true", help="Silent mode")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--save", action="store_true", help="Save results")
    parser.add_argument("--top-ports", action="store_true", help="Scan top ports only")
    parser.add_argument("--full", action="store_true", help="Full scan (for ports)")
    parser.add_argument("--wordlist", help="Path to wordlist")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    framework = AspenFramework(args)

    if args.command == "enum":
        framework.enumerate_subdomains(args.domain)
    elif args.command == "scan":
        framework.scan_ports(args.target)
    elif args.command == "tech":
        tech = framework.fingerprint_tech(args.url)
        console.print(json.dumps(tech, indent=4))
    elif args.command == "screenshot":
        framework.take_screenshot(args.url)
    elif args.command == "vulns":
        report = framework.map_vulns(args.url)
        console.print(report)
    elif args.command == "fullscan":
        framework.full_scan(args.domain)

if __name__ == "__main__":
    main()
