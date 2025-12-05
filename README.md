
# Aspen-Framework

**Aspen-Framework** is an **Automated Reconnaissance Framework** for ethical security testing. It is designed for security researchers and pentesters to perform reconnaissance efficiently.  

> ⚠️ **Warning:** Use only for authorized security testing. Unauthorized scanning is illegal.

---

## Features

- **Subdomain Enumeration**  
  - DNS brute-force  
  - CRT.sh integration  
  - Passive DNS (API required)  
  - Google dorks  

- **Port Scanning**  
  - Top ports or full range  
  - Service detection  

- **Technology Fingerprinting**  
  - Detect server type, language, CMS, and security headers  

- **Screenshotting**  
  - Headless browser screenshots  

- **Vulnerability Mapping**  
  - Missing security headers  
  - Directory listing  
  - Default server pages  
  - Outdated servers  

- **SSL Certificate Scanning**  
  - Main domains and subdomains  

- **Full Scan**  
  - Run all modules together with a single command  

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/alhamrizvi-cloud/Aspen-Framework.git
cd Aspen-Framework
````

### 2. Create and activate a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install a browser driver for Selenium

Aspen uses Selenium for screenshots:

```bash
sudo apt install chromium-driver      # Debian/Ubuntu/Parrot OS
# or manually download ChromeDriver for your version
```

---

## Usage

### CLI Mode

Run Aspen from the command line:

```bash
python3 aspen.py <command> [options]
```

#### Examples:

* **Subdomain enumeration**

```bash
python3 aspen.py enum --domain example.com --crt
```

* **Port scanning (top ports)**

```bash
python3 aspen.py scan --target example.com --top-ports
```

* **Technology fingerprinting**

```bash
python3 aspen.py tech --url http://example.com
```

* **Take a screenshot**

```bash
python3 aspen.py screenshot --url http://example.com
```

* **Vulnerability mapping**

```bash
python3 aspen.py vulns --url http://example.com
```

* **SSL scanning**

```bash
python3 aspen.py ssl --domain example.com
```

* **Full scan (all modules)**

```bash
python3 aspen.py fullscan --domain example.com
```

---

### Web Mode

```bash
python3 aspen.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to access the web interface.

---

## Directory Structure

```
Aspen-Framework/
├── aspen.py              # Main CLI entry point
├── requirements.txt      # Python dependencies
├── results/              # Scan results

---

## Notes

* Ensure **ChromeDriver** or **ChromiumDriver** is installed for screenshots.
* Logs are saved in `logs/aspen.log`.
* Scan results are saved in `results/`.
* Optional: Use a custom **wordlist** for subdomain enumeration.
* Only scan targets you have explicit permission to test.

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Author

**Alham Rizvi**



