---
description: Execute complete security operation - AI takes full control and executes everything automatically
---

# 🛡️ FULL OPERATION - Automated Security Operation

This workflow allows the AI to take **full control** of a security operation, executing all phases automatically and making real-time decisions.

## Activation

User simply says (any language):
- "Full operation against example.com"
- "Pentest example.com"
- "Pentest on 192.168.1.0/24"
- "Hack testsite.com"
- "Attack the production API"
- "Red team client-xyz.com"
- "Penetration test example.com"
- "Security assessment of example.com"

## Automatic Execution Phases

### PHASE 1: 🔴 RedTeam - Reconnaissance
// turbo
```bash
secteam new "$(echo $TARGET | tr '.' '-')-$(date +%Y%m%d)"
```

The AI will automatically execute:
1. **Passive reconnaissance**: whois, DNS, subdomains, certificates
2. **Active reconnaissance**: nmap, masscan, ports and services
3. **Web enumeration**: ffuf, gobuster, directories and files
4. **Fingerprinting**: technologies, versions, WAF detection

### PHASE 2: 🔴 RedTeam - Vulnerability Analysis
The AI will execute:
1. **Automated scanning**: nuclei, nikto, wapiti
2. **Manual analysis**: interesting endpoints, parameters
3. **CVE identification**: searchsploit, vulners
4. **Prioritization**: order by criticality and exploitability

### PHASE 3: 🔴 RedTeam - Exploitation
The AI will decide and execute:
1. **Exploit selection**: based on found vulnerabilities
2. **Payload preparation**: adapt to target
3. **Controlled execution**: attempt exploitation
4. **Documentation**: capture evidence of each attempt

### PHASE 4: 🔴 RedTeam - Post-Exploitation (if access obtained)
1. **Internal enumeration**: users, permissions, network
2. **Privilege escalation**: find paths
3. **Lateral movement**: identify other systems
4. **Persistence**: document methods (don't implement without authorization)

### PHASE 5: 🔵 BlueTeam - Detection Analysis
The AI will analyze:
1. **Generated logs**: what was detected from the attack
2. **SIEM alerts**: event correlation
3. **Detection gaps**: what was NOT detected
4. **IOCs**: identified indicators of compromise

### PHASE 6: 🟣 PurpleTeam - Validation
The AI will map:
1. **MITRE ATT&CK**: techniques used
2. **Detections vs Attacks**: coverage matrix
3. **Identified gaps**: security breaches
4. **Recommendations**: detection improvements

### PHASE 7: 🟢 GreenTeam - Code Analysis (if applicable)
1. **SAST**: static code analysis
2. **Secrets**: search for hardcoded credentials
3. **Dependencies**: vulnerabilities in libraries
4. **IaC**: infrastructure misconfigurations

### PHASE 8: 📊 Mega Report Generation
// turbo
```bash
secteam report "$PROJECT_NAME" --full
```

## AI Autonomous Decisions

The AI will make decisions based on:

| Situation | Decision |
|-----------|----------|
| Port 80/443 open | Execute full web scan |
| Port 22 open | Attempt SSH enumeration, search for credentials |
| Port 3306/5432 open | Test default credentials |
| Critical vulnerability found | Attempt immediate exploitation |
| WAF detected | Apply bypass techniques |
| Access obtained | Proceed with post-exploitation |
| No web vulnerabilities | Pivot to other vectors |

## Execution Example

```
User: "Pentest testsite.com"

AI: 🛡️ Starting FULL OPERATION against testsite.com
    
    📁 Creating project: testsite-com-20240504
    
    ═══ PHASE 1: RECONNAISSANCE ═══
    🔴 [RedTeam] Executing passive reconnaissance...
    > whois testsite.com
    > dig testsite.com ANY
    > subfinder -d testsite.com
    
    🔴 [RedTeam] Executing active reconnaissance...
    > nmap -sV -sC -p- testsite.com
    [+] Ports found: 22, 80, 443, 3306
    
    ═══ PHASE 2: VULNERABILITY ANALYSIS ═══
    🔴 [RedTeam] Scanning vulnerabilities...
    > nuclei -u https://testsite.com -t cves/
    [CRITICAL] CVE-2024-XXXX detected at /api/upload
    
    ═══ PHASE 3: EXPLOITATION ═══
    🔴 [RedTeam] Attempting to exploit CVE-2024-XXXX...
    > [payload executed]
    [+] Access obtained! Shell as www-data
    
    ═══ PHASE 4: POST-EXPLOITATION ═══
    🔴 [RedTeam] Enumerating system...
    > id && whoami && uname -a
    > cat /etc/passwd
    [+] mysql user found with DB access
    
    ═══ PHASE 5: DEFENSIVE ANALYSIS ═══
    🔵 [BlueTeam] Analyzing detections...
    [!] WAF did not block the payload
    [!] No SIEM alerts for this attack
    
    ═══ PHASE 6: VALIDATION ═══
    🟣 [PurpleTeam] Mapping to MITRE ATT&CK...
    - T1190: Exploit Public-Facing Application
    - T1059: Command and Scripting Interpreter
    - T1083: File and Directory Discovery
    
    ═══ PHASE 7: REPORT ═══
    📊 Generating mega report...
    [+] Report saved to: reports/testsite-com-20240504/
    
    ✅ FULL OPERATION COMPLETED
    
    Summary:
    - Critical vulnerabilities: 1
    - Access obtained: 1 (www-data)
    - Detection gaps: 3
    - Recommendations: 5
```

## Commands the AI Can Execute

### Reconnaissance
```bash
nmap -sV -sC -p- $TARGET
masscan -p1-65535 $TARGET --rate=1000
subfinder -d $TARGET
amass enum -d $TARGET
whatweb $TARGET
wafw00f $TARGET
```

### Vulnerability Scanning
```bash
nuclei -u $TARGET -t cves/ -t vulnerabilities/
nikto -h $TARGET
wapiti -u $TARGET
sqlmap -u "$TARGET/page?id=1" --batch
```

### Exploitation
```bash
msfconsole -q -x "use exploit/...; set RHOSTS $TARGET; run"
searchsploit $SERVICE $VERSION
```

### Defensive Analysis
```bash
grep -r "attack_pattern" /var/log/
suricata -r capture.pcap
yara -r rules/ samples/
```

## Important Notes

1. **Authorization**: This workflow assumes full authorization
2. **Scope**: The AI will respect the defined scope
3. **Documentation**: Everything is documented automatically
4. **Reversibility**: No destructive changes without confirmation
