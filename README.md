
<img width="1021" height="762" alt="image" src="https://github.com/user-attachments/assets/c3655be8-a54f-422e-ab84-fff3d57efa20" />
# Aspen-Framework

**Aspen-Framework** is an **Automated Reconnaissance Framework** for ethical security testing.  
It helps security researchers and penetration testers perform reconnaissance quickly and efficiently.

> ⚠️ Use this tool only for authorized testing. Unauthorized scanning is illegal.

---

## Features

- **Subdomain Enumeration**
  - DNS brute-force
  - CRT.sh certificate transparency scraping
  - Passive DNS (optional APIs)
  - Google dork fallback

- **Port Scanning**
  - Top ports scan
  - Full port scan (requires sudo)
  - Service detection

- **Technology Fingerprinting**
  - Detect server type
  - Detect backend language
  - CMS detection
  - Security headers detection

- **Screenshotting**
  - Headless browser screenshots via Selenium

- **Vulnerability Mapping**
  - Missing security headers
  - Directory listing detection
  - Default server page detection
  - Basic outdated server identification

- **Full Scan**
  - Execute all modules in one command

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/alhamrizvi-cloud/Aspen-Framework.git
cd Aspen-Framework
```

### 2. Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install browser driver (required for screenshots)

```bash
sudo apt install chromium-driver
```

Or download ChromeDriver manually for your browser version.

---

## Usage

Run this to see available commands:

```bash
python3 aspen.py
```

---

## Commands

### 1. Subdomain Enumeration

```bash
python3 aspen.py enum --domain example.com --save --wordlist wordlists/subdomains.txt
```

---

### 2. Port Scan

**Top ports**

```bash
python3 aspen.py scan --domain example.com --top-ports
```

**Full port scan (requires sudo)**

```bash
sudo python3 aspen.py scan --domain example.com --full
```

---

### 3. Technology Fingerprinting

```bash
python3 aspen.py tech --domain example.com --save
```

---

### 4. Screenshot

```bash
python3 aspen.py screenshot --domain example.com --save
```

---

### 5. Vulnerability Scan

```bash
python3 aspen.py vulns --domain example.com --save
```

---

### 6. Full Automatic Recon (Recommended)

```bash
python3 aspen.py fullscan --domain example.com --full --save --wordlist wordlists/subdomains.txt
```

---

## Output Structure

```
Aspen-Framework/
 ├── results/
 │   ├── subdomains_<domain>.txt
 │   ├── tech_<domain>.json
 │   ├── vulns_<domain>.txt
 ├── screenshots/
 │   ├── <domain>.png
 ├── logs/
```

---

## Directory Structure

```
Aspen-Framework/
├── aspen.py
├── requirements.txt
├── results/
├── screenshots/
├── logs/
└── wordlists/
```

---

## Notes

- ChromeDriver or ChromiumDriver is required for screenshots.
- Logs are stored in `logs/aspen.log`.
- Results are stored in `results/`.
- You may use any custom subdomain wordlist.
- Only scan targets you have permission to test.

---

## Contributing

1. Fork this repository  
2. Create a feature branch:  
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:  
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request  

---

## License

This project is licensed under the MIT License.

---

## Author

**Alham Rizvi**





