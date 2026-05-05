# 🛡️ Security Team Workspace - Quick Start Guide

Welcome to the **Security Team Workspace**! This guide will help you run your first autonomous security operation.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [First Run Demo](#first-run-demo)
3. [Full Operation Example](#full-operation-example)
4. [Understanding the Output](#understanding-the-output)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before running your first operation, ensure you have:

```bash
# 1. Make secteam executable
chmod +x secteam

# 2. Verify installation
./secteam status

# 3. (Optional) Install tools for full functionality
sudo ./install.sh --full
```

### Minimum Required Tools

For basic operations, you need at least:
- `nmap` - Port scanning
- `curl` - HTTP requests
- `dig` / `whois` - DNS reconnaissance

```bash
# Quick install on Kali/Debian
sudo apt install nmap curl dnsutils whois -y
```

---

## 🚀 First Run Demo

### Option 1: Using AI Assistant (Recommended)

Simply open this workspace in your AI-powered IDE (Windsurf, Cursor, Copilot, etc.) and say:

```
Pentest testphp.vulnweb.com
```

or

```
Full operation against testphp.vulnweb.com
```

The AI will:
1. ✅ Create a new project automatically
2. ✅ Run reconnaissance (ports, services, technologies)
3. ✅ Scan for vulnerabilities
4. ✅ Attempt exploitation if vulnerabilities found
5. ✅ Analyze defensive gaps
6. ✅ Generate a comprehensive report

### Option 2: Manual Step-by-Step

```bash
# 1. Create a new project
./secteam new demo-vulnweb

# 2. Activate RedTeam
./secteam red

# 3. Run reconnaissance manually
nmap -sV -sC testphp.vulnweb.com

# 4. Generate report
./secteam report demo-vulnweb
```

---

## 🎯 Full Operation Example

### Target: Acunetix Vulnerable Web Application

We'll use **testphp.vulnweb.com** - a deliberately vulnerable website for testing.

> ⚠️ **IMPORTANT**: This is a legal test target provided by Acunetix for security testing practice.

### Step 1: Trigger Full Operation

In your AI IDE, simply say:

```
Full operation against testphp.vulnweb.com
```

### Step 2: Watch the AI Work

The AI will execute the following phases automatically:

```
═══════════════════════════════════════════════════════════════════
🛡️ FULL OPERATION: testphp.vulnweb.com
═══════════════════════════════════════════════════════════════════

📁 Creating project: testphp-vulnweb-com-20240505

═══ PHASE 1: RECONNAISSANCE ═══
🔴 [RedTeam] Passive reconnaissance...
   > whois vulnweb.com
   > dig testphp.vulnweb.com ANY
   
🔴 [RedTeam] Active reconnaissance...
   > nmap -sV -sC -p- testphp.vulnweb.com
   [+] Open ports: 80 (http)
   [+] Server: nginx
   [+] Technology: PHP

🔴 [RedTeam] Web enumeration...
   > curl -I https://testphp.vulnweb.com
   > Checking for mobile app indicators...
   [?] Mobile app detected? Checking /api/, app store links...

═══ PHASE 2: VULNERABILITY SCANNING ═══
🔴 [RedTeam] Scanning for vulnerabilities...
   > nuclei -u http://testphp.vulnweb.com
   [CRITICAL] SQL Injection in /listproducts.php?cat=
   [HIGH] XSS in /search.php?test=
   [MEDIUM] Directory listing enabled

═══ PHASE 3: EXPLOITATION ═══
🔴 [RedTeam] Exploiting SQL Injection...
   > sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1"
   [+] Database: acuart
   [+] Tables: artists, carts, categ, featured, guestbook, pictures, products, users
   [+] Users table dumped!

═══ PHASE 4: DEFENSIVE ANALYSIS ═══
🔵 [BlueTeam] Analyzing what would be detected...
   [!] No WAF detected
   [!] SQL errors exposed to users
   [!] No rate limiting

═══ PHASE 5: MITRE ATT&CK MAPPING ═══
🟣 [PurpleTeam] Techniques used:
   - T1190: Exploit Public-Facing Application
   - T1059: Command and Scripting Interpreter
   - T1005: Data from Local System

═══ PHASE 6: REPORT GENERATION ═══
📊 Generating comprehensive report...
   [+] Report saved: reports/testphp-vulnweb-com-20240505/

✅ OPERATION COMPLETED

Summary:
├── Critical vulnerabilities: 1 (SQLi)
├── High vulnerabilities: 1 (XSS)
├── Medium vulnerabilities: 1 (Directory listing)
├── Access obtained: Database dump
├── Detection gaps: 3
└── Recommendations: 5
```

### Step 3: Review the Report

```bash
# View the generated report
cat reports/testphp-vulnweb-com-*/FULL_REPORT.md
```

---

## 📱 Mobile App Detection

RedTeam automatically checks for mobile app presence:

### Automatic Detection
The AI looks for:
- `/api/` endpoints (REST APIs)
- App store links in HTML
- `mobile`, `app`, `ios`, `android` references
- API documentation endpoints
- JWT/OAuth endpoints

### If Mobile App Detected

```
🔴 [RedTeam] Mobile app indicators found!
   [+] API endpoint: /api/v1/
   [+] iOS app link detected
   [+] Android app link detected
   
   Expanding attack surface:
   > Testing API endpoints
   > Checking for API key exposure
   > Testing authentication bypass
   > Looking for sensitive data exposure
```

### Manual Mobile Check

If you want to explicitly include mobile testing:

```
Pentest testphp.vulnweb.com including mobile app analysis
```

or

```
Full operation against example.com - check for mobile apps too
```

---

## 📊 Understanding the Output

### Severity Levels

| Level | Color | Meaning |
|-------|-------|---------|
| 🔴 CRITICAL | Red | Immediate exploitation possible, high impact |
| 🟠 HIGH | Orange | Significant risk, should fix soon |
| 🟡 MEDIUM | Yellow | Moderate risk, plan to fix |
| 🟢 LOW | Green | Minor issue, fix when possible |

### Report Sections

| Section | Description |
|---------|-------------|
| `EXECUTIVE_SUMMARY.md` | High-level overview for management |
| `FULL_REPORT.md` | Complete technical details |
| `findings/` | Vulnerabilities organized by severity |
| `evidence/` | Screenshots, logs, proof of concepts |
| `exploits/` | Payloads and exploit code used |
| `credentials/` | Any credentials obtained |
| `REMEDIATION.md` | Fix recommendations with priority |

---

## 🔧 Troubleshooting

### "Command not found: secteam"

```bash
# Make sure you're in the workspace directory
cd /path/to/Security-Team---Workspace-

# Make executable
chmod +x secteam

# Run with ./
./secteam status
```

### "nmap/nuclei not installed"

```bash
# Install basic tools
sudo apt update
sudo apt install nmap -y

# Install nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

### AI doesn't execute commands

Make sure your IDE rules are loaded:
1. Close and reopen the workspace
2. Check that `.windsurfrules` (or equivalent) exists
3. Try saying: "Read the .windsurfrules file and confirm you understand"

### No output from scans

```bash
# Test connectivity
ping testphp.vulnweb.com

# Test with curl
curl -I http://testphp.vulnweb.com
```

---

## 🎓 Next Steps

After your first successful operation:

1. **Try different targets** (always with authorization!)
2. **Explore team-specific commands**: `./secteam blue`, `./secteam purple`
3. **Create custom workflows** in `.windsurf/workflows/`
4. **Share findings between teams**: `./secteam share BlueTeam finding.md`

---

## 📚 Quick Reference

### Trigger Phrases (Any Language)

| Action | Phrases |
|--------|---------|
| Full pentest | "Pentest [target]", "Full operation against [target]" |
| Recon only | "Reconnaissance on [target]", "Scan [target]" |
| Web attacks | "Test web vulnerabilities on [target]" |
| Code scan | "Scan this code for vulnerabilities" |
| Threat model | "Create threat model for this application" |

### Orchestrator Commands

```bash
./secteam status          # View workspace state
./secteam new <name>      # Create project
./secteam red             # Activate RedTeam
./secteam blue            # Activate BlueTeam
./secteam report <name>   # Generate report
./secteam help            # Show all commands
```

---

<p align="center">
  <strong>🛡️ Ready to break things? Let's go! 🚀</strong>
</p>
