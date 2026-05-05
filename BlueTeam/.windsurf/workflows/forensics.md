---
description: Digital forensics analysis workflow
---

# /forensics - Forensic Analysis Workflow

Análisis forense digital completo.

## Uso
```
/forensics [type] [target]
```

## Tipos de análisis:
- `collect` - Recolectar artefactos
- `memory` - Análisis de memoria
- `disk` - Análisis de disco
- `network` - Análisis de red
- `timeline` - Crear timeline
- `malware` - Análisis de malware

## Ejemplos:
- `/forensics collect`
- `/forensics memory /path/to/dump.raw`
- `/forensics timeline /var/log`
- `/forensics malware /tmp/suspicious_file`

## Pasos del Workflow

### 1. Recolección de Evidencia
// turbo
```bash
cd ~/Documents/BlueTeam\ -\ KaliLinux && sudo ./tools/custom-scripts/forensic_collector.sh --collect-all --package
```

### 2. Análisis de Memoria (si hay dump)

#### Con Volatility 3:
```bash
# Listar procesos
vol3 -f memory.dmp windows.pslist

# Conexiones de red
vol3 -f memory.dmp windows.netscan

# Buscar malware
vol3 -f memory.dmp windows.malfind

# Línea de comandos
vol3 -f memory.dmp windows.cmdline

# DLLs cargadas
vol3 -f memory.dmp windows.dlllist
```

#### Para Linux:
```bash
vol3 -f memory.dmp linux.pslist
vol3 -f memory.dmp linux.bash
vol3 -f memory.dmp linux.lsof
```

### 3. Análisis de Disco

#### Con Sleuth Kit:
```bash
# Listar particiones
mmls disk.img

# Listar archivos
fls -r disk.img

# Extraer archivo
icat disk.img <inode> > extracted_file

# Timeline del filesystem
fls -r -m "/" disk.img > bodyfile.txt
mactime -b bodyfile.txt > timeline.txt
```

#### Con Autopsy:
```bash
autopsy
# Abrir en navegador: http://localhost:9999/autopsy
```

### 4. Análisis de Red

#### Captura de tráfico:
```bash
tcpdump -i eth0 -w capture.pcap
```

#### Análisis con tshark:
```bash
# Estadísticas de conversaciones
tshark -r capture.pcap -q -z conv,tcp

# Extraer archivos
tshark -r capture.pcap --export-objects http,./extracted/

# Buscar patrones
tshark -r capture.pcap -Y "http.request.method == POST"
```

#### Análisis con Zeek:
```bash
zeek -r capture.pcap
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p
```

### 5. Crear Timeline

```bash
# Usando plaso/log2timeline
log2timeline.py timeline.plaso /path/to/evidence

# Generar timeline
psort.py -o l2tcsv timeline.plaso > timeline.csv
```

### 6. Análisis de Malware

#### Análisis estático:
```bash
# Información del archivo
file suspicious_file
exiftool suspicious_file

# Strings
strings -n 8 suspicious_file | head -100

# Hashes
md5sum suspicious_file
sha256sum suspicious_file

# Escaneo YARA
yara -r rules/yara/*.yar suspicious_file

# Escaneo antivirus
clamscan suspicious_file
```

#### Análisis dinámico (sandbox):
```bash
# Con Cuckoo (si está configurado)
cuckoo submit suspicious_file
```

### 7. Generar Reporte Forense

El reporte debe incluir:
1. Resumen ejecutivo
2. Metodología utilizada
3. Timeline de eventos
4. Artefactos analizados
5. IOCs identificados
6. Conclusiones
7. Recomendaciones

## Artefactos Clave por Sistema

### Linux:
| Artefacto | Ubicación | Información |
|-----------|-----------|-------------|
| Auth logs | /var/log/auth.log | Autenticación |
| Syslog | /var/log/syslog | Sistema |
| Bash history | ~/.bash_history | Comandos |
| Crontabs | /var/spool/cron | Tareas programadas |
| SSH keys | ~/.ssh/ | Acceso remoto |
| /etc/passwd | /etc/passwd | Usuarios |
| Processes | /proc/ | Procesos activos |

### Windows:
| Artefacto | Ubicación | Información |
|-----------|-----------|-------------|
| Event Logs | C:\Windows\System32\winevt | Eventos |
| Registry | C:\Windows\System32\config | Configuración |
| Prefetch | C:\Windows\Prefetch | Ejecución |
| $MFT | C:\ | Filesystem |
| Amcache | C:\Windows\AppCompat | Aplicaciones |
| NTUSER.DAT | C:\Users\*\ | Usuario |

## Cadena de Custodia

Documentar siempre:
1. Quién recolectó la evidencia
2. Cuándo se recolectó
3. Cómo se recolectó
4. Hash de la evidencia
5. Dónde se almacena

## Output Esperado

```
🔬 Forensic Analysis Report
═══════════════════════════════════════════════════════════════

📋 Case Information:
   • Case ID: FOR-2024-0001
   • Analyst: security_analyst
   • Date: 2024-01-15
   • Evidence Hash: sha256:a1b2c3d4...

📊 Evidence Collected:
   • System artifacts: 45 files
   • Log files: 12 files
   • Memory dump: 4GB
   • Network capture: 500MB

🕐 Timeline Summary:
   • First malicious activity: 2024-01-14 22:15:00
   • Initial access: SSH brute force
   • Privilege escalation: 2024-01-14 22:30:00
   • Data exfiltration: 2024-01-15 01:00:00

🔍 Key Findings:
   1. Attacker gained access via compromised SSH credentials
   2. Escalated to root using CVE-2021-4034
   3. Installed backdoor in /usr/local/bin/
   4. Exfiltrated 2GB of data to 45.33.32.156

🎯 IOCs:
   • IP: 45.33.32.156
   • Hash: a1b2c3d4e5f6...
   • File: /usr/local/bin/systemd-helper
   • Domain: exfil.evil.com

📋 Recommendations:
   1. Block attacker infrastructure
   2. Patch CVE-2021-4034
   3. Reset all credentials
   4. Deploy EDR solution
   5. Implement MFA for SSH
```
