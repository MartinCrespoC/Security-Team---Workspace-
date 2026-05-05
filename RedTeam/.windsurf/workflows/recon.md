---
description: Workflow de reconocimiento completo para Red Team
---

# 🔍 Reconocimiento - Workflow

## Fase 1: Reconocimiento Pasivo (OSINT)

### 1.1 Información del dominio
```bash
# Whois lookup
whois <DOMAIN>

# DNS records
dig <DOMAIN> ANY +noall +answer
dig <DOMAIN> MX +short
dig <DOMAIN> NS +short
dig <DOMAIN> TXT +short

# Subdomain enumeration pasiva
amass enum -passive -d <DOMAIN> -o recon/passive/subdomains.txt
subfinder -d <DOMAIN> -o recon/passive/subfinder.txt
```

### 1.2 Búsqueda de información expuesta
```bash
# Google Dorks (manual en navegador)
# site:<DOMAIN> filetype:pdf
# site:<DOMAIN> inurl:admin
# site:<DOMAIN> intitle:"index of"

# theHarvester
theHarvester -d <DOMAIN> -b all -f recon/osint/harvester_report

# Shodan (requiere API key)
shodan search hostname:<DOMAIN>
```

### 1.3 Redes sociales y empleados
```bash
# LinkedIn scraping (manual)
# Buscar empleados, tecnologías mencionadas

# Metadata de documentos
exiftool -r -ext pdf -ext doc -ext docx <DOWNLOADED_FILES>
```

## Fase 2: Reconocimiento Activo

### 2.1 Descubrimiento de hosts
```bash
# Ping sweep
nmap -sn <NETWORK>/24 -oG recon/active/hosts_alive.txt

# ARP scan (red local)
sudo arp-scan -l -I eth0
```

### 2.2 Escaneo de puertos
```bash
# Escaneo rápido top 1000
nmap -sC -sV -oA recon/active/quick_scan <TARGET>

# Escaneo completo todos los puertos
// turbo
nmap -p- -sC -sV -oA recon/active/full_scan <TARGET>

# Escaneo UDP (más lento)
sudo nmap -sU --top-ports 100 -oA recon/active/udp_scan <TARGET>
```

### 2.3 Enumeración de servicios
```bash
# Web
nikto -h http://<TARGET> -o recon/active/nikto.txt
whatweb http://<TARGET>
gobuster dir -u http://<TARGET> -w /usr/share/wordlists/dirb/common.txt -o recon/active/gobuster.txt

# SMB
enum4linux -a <TARGET> | tee recon/active/enum4linux.txt
smbclient -L //<TARGET> -N
crackmapexec smb <TARGET>

# LDAP
ldapsearch -x -H ldap://<TARGET> -b "dc=domain,dc=com"
```

## Fase 3: Análisis de vulnerabilidades

```bash
# Nmap scripts de vulnerabilidades
nmap --script vuln -oA recon/active/vuln_scan <TARGET>

# Nuclei
nuclei -u http://<TARGET> -o recon/active/nuclei.txt

# Searchsploit para servicios encontrados
searchsploit <SERVICE> <VERSION>
```

## Output esperado
- `recon/passive/` - Información OSINT
- `recon/active/` - Resultados de escaneos
- `recon/osint/` - Reportes de herramientas OSINT
