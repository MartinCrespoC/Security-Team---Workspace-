<div align="center">

# 🔥 RedTeam-Windsurf

<img src="https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Metasploit-E34F26?style=for-the-badge&logo=metasploit&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />

```
██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                    ZERO DAY HUNTER
```

### 🎯 Autonomous Red Team Workspace for Kali Linux + Windsurf AI

**200+ offensive security tools | AI-powered pentesting | One command to pwn**

[Installation](#-installation) • [PWN Command](#-pwn-command) • [Tools](#-tools) • [Scripts](#-custom-scripts)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered** | Cascade agent executes attacks automatically |
| ⚡ **`pwn` Command** | One command for complete pentesting |
| 🛡️ **WAF Bypass** | Cloudflare and WAF evasion scripts |
| 🔍 **Zero-Day Hunting** | Methodology for unique vulnerabilities |
| 📊 **Auto Reports** | Professional report generation |
| 🔧 **200+ Tools** | Complete offensive arsenal |

---

## 📦 Installation

```bash
git clone https://github.com/MartinCrespoC/RedTeam-Windsurf.git
cd RedTeam-Windsurf
chmod +x install.sh
sudo ./install.sh
```

---

## ⚡ PWN Command

```bash
pwn <target>
```

```bash
pwn https://example.com    # Full URL
pwn 192.168.1.100          # IP address
pwn domain.com             # Domain
```

### Attack Pipeline

| Phase | Tool | Action |
|-------|------|--------|
| 1 | subfinder | Subdomains |
| 2 | nmap | Ports & services |
| 3 | httpx | Live hosts |
| 4 | nuclei | Vulnerabilities |
| 5 | ffuf | Directory fuzzing |
| 6 | sqlmap | SQL Injection |
| 7 | searchsploit | Exploits |

---

## 🛠️ Tools

### 🔍 Reconnaissance
`nmap` `masscan` `nuclei` `subfinder` `amass` `httpx` `shodan` `theharvester`

### 🌐 Web
`sqlmap` `ffuf` `gobuster` `nikto` `wpscan` `burpsuite` `dalfox` `commix`

### 💥 Exploitation
`metasploit` `searchsploit` `sliver` `havoc` `beef-xss` `crackmapexec` `bloodhound`

### 🔐 Passwords
`hydra` `john` `hashcat` `crackmapexec`

### 📡 Network
`wireshark` `responder` `chisel` `proxychains4` `tor` `mitmproxy`

### 🤖 MCP Servers
`osint-mcp` `cve-mcp` `kali-mcp-server` `cyberstrike`

---

## 🔥 Custom Scripts

| Script | Description |
|--------|-------------|
| `pwn.sh` | Complete pentesting pipeline |
| `cloudflare_bypass.py` | WAF bypass (cloudscraper, curl_cffi) |
| `cf_origin_finder.sh` | Find origin IP behind Cloudflare |
| `auto_exploit.py` | Auto exploit search (SearchSploit, CVE-MCP) |

---

## 📁 Structure

```
RedTeam-Windsurf/
├── recon/           # Reconnaissance results
├── exploitation/    # Exploits & payloads
├── post-exploitation/
├── web/             # Web attacks (sqli, xss, lfi)
├── network/         # Network operations
├── tools/           # Custom scripts
├── reports/         # Report templates
└── .windsurf/       # AI agent rules
```

---

## 🎮 AI Workflows

| Command | Description |
|---------|-------------|
| `/recon` | Full reconnaissance |
| `/exploitation` | Exploitation phase |
| `/post-exploitation` | Post-exploitation |
| `/web-attacks` | Web application attacks |

---

## 🎯 Zero-Day Hunting Checklist

- [ ] Full subdomain enumeration
- [ ] All ports scan (1-65535)
- [ ] Version fingerprinting
- [ ] Source code analysis
- [ ] Race conditions
- [ ] Business logic flaws
- [ ] Prototype pollution
- [ ] Cache poisoning

---

## ⚠️ Disclaimer

```
For AUTHORIZED environments only.
Unauthorized use is ILLEGAL.
Always get written permission before testing.
```

---

<div align="center">

**🔥 Ready to Hunt Zero-Days 🔥**

Made with ❤️ for Red Team Operations

</div>
