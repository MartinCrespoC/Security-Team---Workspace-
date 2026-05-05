<p align="center">
  <img src="https://img.shields.io/badge/Security-Teams-red?style=for-the-badge&logo=shield&logoColor=white" alt="Security Teams"/>
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/Multi--Agent-Orchestration-purple?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Multi-Agent"/>
</p>

<h1 align="center">🛡️ Security Team by ConcordIA / TITAN</h1>

<p align="center">
  <strong>The first cybersecurity framework with 7 specialized AI agent teams working in parallel with isolated contexts</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/RedTeam-Offensive-red?style=flat-square" alt="RedTeam"/>
  <img src="https://img.shields.io/badge/BlueTeam-Defensive-blue?style=flat-square" alt="BlueTeam"/>
  <img src="https://img.shields.io/badge/PurpleTeam-Validation-purple?style=flat-square" alt="PurpleTeam"/>
  <img src="https://img.shields.io/badge/GreenTeam-DevSecOps-green?style=flat-square" alt="GreenTeam"/>
  <img src="https://img.shields.io/badge/WhiteTeam-GRC-white?style=flat-square" alt="WhiteTeam"/>
  <img src="https://img.shields.io/badge/YellowTeam-Architecture-yellow?style=flat-square" alt="YellowTeam"/>
  <img src="https://img.shields.io/badge/OrangeTeam-Awareness-orange?style=flat-square" alt="OrangeTeam"/>
</p>

<p align="center">
  <a href="#-full-operation-mode">Full Operation</a> •
  <a href="#-features">Features</a> •
  <a href="#-teams">Teams</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-reports">Reports</a>
</p>

---

## 🎯 What is Security Team by ConcordIA / TITAN?

**Security Team by ConcordIA / TITAN** is a revolutionary framework that orchestrates **7 specialized AI security teams**. Each team operates with its own isolated context, but they can communicate and collaborate in real-time to execute complex security operations.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   🛡️ SECURITY TEAM by ConcordIA / TITAN                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🔴 RedTeam    🔵 BlueTeam    🟣 PurpleTeam    🟢 GreenTeam               │
│   ═══════════   ═══════════    ═════════════    ═══════════                │
│   Pentesting    Detection      Validation       DevSecOps                  │
│   Exploitation  Response       Simulation       SAST/DAST                  │
│   Recon         Forensics      Gap Analysis     Container Sec              │
│                                                                             │
│   ⚪ WhiteTeam    🟡 YellowTeam    🟠 OrangeTeam                           │
│   ═══════════     ═════════════    ═════════════                           │
│   Compliance      Architecture     Awareness                               │
│   Risk Mgmt       Threat Model     Phishing Sim                            │
│   Audit           Zero Trust       Training                                │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Isolated Contexts  ✅ Inter-Team Communication  ✅ Unified Reports      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 FULL OPERATION MODE (Auto-Pilot)

**The most powerful feature:** The AI takes full control and executes complete security operations autonomously.

### Natural Language Triggers (Any Language):

| Language | Triggers |
|----------|----------|
| **English** | "Full operation against [target]", "Pentest [target]", "Hack [target]", "Attack [target]", "Pwn [target]", "Red team [target]", "Penetration test [target]" |
| **Spanish** | "Full operation contra [target]", "Pentest de [target]", "Hackea [target]", "Ataca [target]" |
| **Portuguese** | "Pentest em [target]", "Ataque [target]" |
| **French** | "Test d'intrusion sur [target]" |
| **German** | "Penetrationstest auf [target]" |

### Example Execution:

```
User: "Pentest example.com"

🤖 AI: Taking full control...

═══ PHASE 1: RECONNAISSANCE ═══
🔴 [RedTeam] Running reconnaissance...
> nmap -sV -sC example.com
> subfinder -d example.com
> nuclei -u example.com
[+] 3 subdomains found
[+] Ports: 22, 80, 443, 3306

═══ PHASE 2: VULNERABILITY ANALYSIS ═══
🔴 [RedTeam] Scanning for vulnerabilities...
[CRITICAL] SQLi found at /api/users?id=

═══ PHASE 3: EXPLOITATION ═══
🔴 [RedTeam] Exploiting SQLi...
> sqlmap -u "example.com/api/users?id=1" --dump
[+] Database dumped: 1,547 users

═══ PHASE 4: DEFENSIVE ANALYSIS ═══
🔵 [BlueTeam] Analyzing detections...
[!] WAF did not block the attack
[!] No alerts in logs

═══ PHASE 5: VALIDATION ═══
🟣 [PurpleTeam] Mapping to MITRE ATT&CK...
- T1190: Exploit Public-Facing Application
- T1059: Command Injection

═══ PHASE 6: REPORT ═══
📊 Generating mega report...
[+] Report: reports/example-com-20240504/

✅ OPERATION COMPLETED
```

### AI Decision Matrix:

| Situation | AI Decision |
|-----------|-------------|
| Port 80/443 open | → Full web scan |
| SQLi detected | → Immediate exploitation |
| Access obtained | → Post-exploitation |
| WAF detected | → Bypass techniques |
| No web vulns | → Pivot to other vectors |

---

## ✨ Features

### 🚀 Multi-Agent Parallel Execution
- **7 specialized teams** working simultaneously
- **Completely isolated contexts** per project and team
- **Secure communication** between teams via `secteam share`
- **Intelligent orchestration** that assigns tasks to the right team
- **FULL OPERATION MODE** - AI executes everything automatically

### 🎯 Offensive Capabilities (RedTeam)
- Automated reconnaissance (subdomains, ports, services)
- Vulnerability exploitation (web, network, API)
- Post-exploitation and lateral movement
- Payload generation and bypasses

### 🛡️ Defensive Capabilities (BlueTeam)
- Real-time threat detection
- Forensic incident analysis
- Proactive threat hunting
- SIEM/IDS/IPS integration

### 🔄 Continuous Validation (PurpleTeam)
- MITRE ATT&CK attack simulation
- Detection validation
- Automated gap analysis
- Purple Team exercises

### 📊 Detailed Mega Reports
- **Findings by team** with severity and evidence
- **CVEs and CWEs** identified
- **Exploits and payloads** used
- **Access obtained** and credentials
- **Exposed secrets** found
- **Remediation recommendations**
- **Activity timeline**

---

## 🎨 Teams

<table>
<tr>
<td width="50%">

### 🔴 RedTeam - Offensive Security
**Role:** Break everything that can be broken

**Capabilities:**
- 🔍 Reconnaissance & OSINT
- 🌐 Web Application Attacks
- 🔓 Exploitation & Post-Exploitation
- 🎭 Social Engineering
- 🔑 Credential Attacks
- 🚀 Privilege Escalation

**Tools:**
`metasploit` `nmap` `burpsuite` `sqlmap` `nuclei` `ffuf` `gobuster` `hydra` `john` `hashcat`

</td>
<td width="50%">

### 🔵 BlueTeam - Defensive Security
**Role:** Protect everything that can be protected

**Capabilities:**
- 🔔 Threat Detection
- 🚨 Incident Response
- 🔬 Digital Forensics
- 📊 Log Analysis
- 🕵️ Threat Hunting
- 📡 Network Monitoring

**Tools:**
`wazuh` `suricata` `zeek` `volatility` `yara` `osquery` `velociraptor` `splunk` `elastic`

</td>
</tr>
<tr>
<td width="50%">

### 🟣 PurpleTeam - Security Validation
**Role:** Validate attacks and detections

**Capabilities:**
- ⚔️ Attack Simulation
- ✅ Detection Validation
- 📉 Gap Analysis
- 🗺️ MITRE ATT&CK Mapping
- 🔄 Continuous Validation

**Tools:**
`caldera` `atomic-red-team` `dettect` `attack-navigator` `vectr` `infection-monkey`

</td>
<td width="50%">

### 🟢 GreenTeam - DevSecOps
**Role:** Security in development

**Capabilities:**
- 🔍 SAST (Static Analysis)
- 🌐 DAST (Dynamic Analysis)
- 📦 SCA (Dependency Check)
- 🐳 Container Security
- 🏗️ IaC Security
- 🔐 Secret Detection

**Tools:**
`semgrep` `trivy` `gitleaks` `checkov` `snyk` `zap` `nuclei` `grype` `hadolint`

</td>
</tr>
<tr>
<td width="50%">

### ⚪ WhiteTeam - GRC
**Role:** Governance, Risk & Compliance

**Capabilities:**
- 📋 Compliance Audits
- ⚠️ Risk Assessment
- 📜 Policy Management
- 📊 Evidence Collection
- 🎯 Control Mapping

**Frameworks:**
`ISO 27001` `NIST` `SOC2` `PCI-DSS` `HIPAA` `GDPR` `CIS Controls`

</td>
<td width="50%">

### 🟡 YellowTeam - Security Architecture
**Role:** Secure design from the start

**Capabilities:**
- 🎯 Threat Modeling (STRIDE)
- 🏛️ Architecture Review
- 📋 Security Requirements
- 🔒 Zero Trust Design
- 📐 Secure Patterns

**Tools:**
`pytm` `threat-dragon` `diagrams` `draw.io` `plantuml`

</td>
</tr>
<tr>
<td colspan="2">

### 🟠 OrangeTeam - Security Awareness
**Role:** The human factor

**Capabilities:**
- 🎣 Phishing Simulation
- 📚 Security Training
- 📊 Awareness Metrics
- 🎭 Social Engineering Tests
- 📈 Campaign Analytics

**Tools:**
`gophish` `king-phisher` `set` `beef` `evilginx2`

</td>
</tr>
</table>

---

## 🚀 Installation

### Prerequisites
- Linux (Kali Linux recommended)
- Python 3.8+
- Docker & Docker Compose
- Git

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/MartinCrespoC/Security-Team---Workspace-.git
cd Security-Team---Workspace-

# Full installation (requires sudo)
sudo ./install.sh --full

# Or interactive installation
sudo ./install.sh
```

### Post-Installation

⚠️ **IMPORTANT:** After installation, configure the required `.env` files:

```bash
# Copy configuration templates
cp RedTeam/.env.example RedTeam/.env
cp BlueTeam/.env.example BlueTeam/.env
cp OrangeTeam/.env.example OrangeTeam/.env

# Edit with your API keys and configurations
nano RedTeam/.env
```

**Common environment variables:**
| Variable | Description | Teams |
|----------|-------------|-------|
| `SHODAN_API_KEY` | Shodan API key | RedTeam |
| `VIRUSTOTAL_API_KEY` | VirusTotal API key | BlueTeam |
| `SLACK_WEBHOOK` | Webhook for notifications | All |
| `SMTP_SERVER` | SMTP server for phishing | OrangeTeam |

---

## 📋 Usage

### Orchestrator Commands

```bash
# View workspace status
secteam status

# Create new project with isolated contexts
secteam new client-project-xyz

# Activate team context
secteam red      # 🔴 Red Team
secteam blue     # 🔵 Blue Team
secteam purple   # 🟣 Purple Team
secteam green    # 🟢 Green Team
secteam white    # ⚪ White Team
secteam yellow   # 🟡 Yellow Team
secteam orange   # 🟠 Orange Team

# Share findings between teams
secteam share BlueTeam vulnerability-report.md

# Generate mega report
secteam report client-project-xyz

# List projects
secteam list
```

### Example: Complete Security Operation

```bash
# 1. Create project
secteam new operation-aurora

# 2. RedTeam: Reconnaissance and exploitation
secteam red
# AI will execute: nmap, nuclei, sqlmap, etc.

# 3. BlueTeam: Analyze detections
secteam blue
# AI will analyze logs and generated alerts

# 4. PurpleTeam: Validate gaps
secteam purple
# AI will map to MITRE ATT&CK

# 5. Generate mega report
secteam report operation-aurora --full
```

---

## 📊 Report System

The framework generates **Mega Reports** with all operation information:

### Report Structure

```
📁 reports/
└── 📁 operation-aurora-20240504/
    ├── 📄 EXECUTIVE_SUMMARY.md
    ├── 📄 FULL_REPORT.md
    ├── 📁 findings/
    │   ├── 📄 critical.md
    │   ├── 📄 high.md
    │   ├── 📄 medium.md
    │   └── 📄 low.md
    ├── 📁 evidence/
    │   ├── 📁 screenshots/
    │   ├── 📁 logs/
    │   └── 📁 payloads/
    ├── 📁 exploits/
    │   ├── 📄 CVE-2024-XXXX.md
    │   └── 📄 custom-exploits.md
    ├── 📁 credentials/
    │   ├── 📄 hashes.txt
    │   ├── 📄 cracked.txt
    │   └── 📄 secrets.md
    └── 📄 REMEDIATION.md
```

### Mega Report Contents

| Section | Content |
|---------|---------|
| **Executive Summary** | High-level summary for executives |
| **Findings** | Vulnerabilities by severity (Critical/High/Medium/Low) |
| **CVEs Identified** | List of CVEs with description and CVSS |
| **CWEs Mapped** | Weaknesses categorized by CWE |
| **Exploits Used** | Code and payloads used |
| **Access Obtained** | Compromised systems and access level |
| **Credentials** | Hashes, cracked passwords, API keys |
| **Exposed Secrets** | Tokens, keys, certificates found |
| **Timeline** | Operation chronology |
| **Responsible Team** | Which team discovered each finding |
| **Remediation** | Recommended fixes with priority |

---

## 🤖 IDE Compatibility

This workspace works with **any AI-powered IDE**:

| IDE/Assistant | Configuration File | Status |
|---------------|-------------------|--------|
| **Windsurf** | `.windsurfrules` | ✅ |
| **Cursor** | `.cursorrules` | ✅ |
| **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ |
| **Cline/Claude Dev** | `.clinerules` | ✅ |
| **Gemini** | `.gemini` | ✅ |
| **Claude** | `CLAUDE.md` | ✅ |

### Using with AI

Simply open the workspace in your IDE and request:

```
"Pentest example.com"
"Analyze these logs for malicious activity"
"Scan the code for vulnerabilities"
"Create a threat model for the application"
"Generate an ISO 27001 compliance report"
```

The AI will automatically identify which team(s) should act and execute the appropriate tools.

---

## 📁 Project Structure

```
Security-Team---Workspace-/
│
├── 🔴 RedTeam/                    # Offensive tools
│   ├── tools/
│   ├── scripts/
│   ├── wordlists/
│   └── .env.example
│
├── 🔵 BlueTeam/                   # Defensive tools
│   ├── rules/
│   ├── playbooks/
│   ├── iocs/
│   └── .env.example
│
├── 🟣 PurpleTeam/                 # Validation
│   ├── atomic-tests/
│   ├── detections/
│   └── mappings/
│
├── 🟢 GreenTeam/                  # DevSecOps
│   ├── scanners/
│   ├── policies/
│   └── pipelines/
│
├── ⚪ WhiteTeam/                  # GRC
│   ├── frameworks/
│   ├── policies/
│   ├── audits/
│   └── templates/
│
├── 🟡 YellowTeam/                 # Architecture
│   ├── threat-models/
│   ├── architectures/
│   └── requirements/
│
├── 🟠 OrangeTeam/                 # Awareness
│   ├── campaigns/
│   ├── training/
│   └── templates/
│
├── 📁 .contexts/                  # Context configuration
│   └── config.json
│
├── 📁 .projects/                  # Projects (isolated contexts)
│
├── 📁 .shared/                    # Shared findings
│
├── 📁 .windsurf/workflows/        # Automation workflows
│
├── 📁 reports/                    # Generated mega reports
│
├── 🔧 secteam                     # CLI Orchestrator
├── 🔧 install.sh                  # Unified installer
├── 📄 .windsurfrules              # Windsurf config
├── 📄 .cursorrules                # Cursor config
├── 📄 .clinerules                 # Cline config
├── 📄 .gemini                     # Gemini config
├── 📄 CLAUDE.md                   # Claude config
├── 📄 LICENSE                     # License
└── 📄 README.md                   # This file
```

---

## ⚠️ Disclaimer

This framework is designed **exclusively for authorized use** in:
- Authorized penetration testing
- Contracted security assessments
- Ethical security research
- Lab environments and CTFs

**Unauthorized use of these tools is illegal and strictly prohibited.**

---

## 📜 License

This project is under the **Security Research License**. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome. Please read the contribution guidelines before submitting a PR.

---

## 👨‍💻 Author

**Martin Crespo**

---

<p align="center">
  <strong>🛡️ Break Everything. Protect Everything. Report Everything. 🛡️</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge" alt="Made with love"/>
</p>
