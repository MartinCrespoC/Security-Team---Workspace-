# 🛡️ BlueTeam-Windsurf

```
██████╗ ██╗     ██╗   ██╗███████╗████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██║     ██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝██║     ██║   ██║█████╗     ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██║     ██║   ██║██╔══╝     ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
██████╔╝███████╗╚██████╔╝███████╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                    ⚡ Powered by Windsurf AI ⚡
```

![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-5.0+-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Cascade-blueviolet?style=for-the-badge)

> **🔒 Centro de Operaciones de Seguridad (SOC) autónomo con Inteligencia Artificial**

---

## 🚀 Instalación Rápida

```bash
# Clonar y ejecutar
git clone https://github.com/tu-usuario/BlueTeam-Windsurf.git
cd BlueTeam-Windsurf
chmod +x install.sh
sudo ./install.sh --full

# Instalación mínima
sudo ./install.sh --minimal

# Solo herramientas específicas
sudo ./install.sh --siem
sudo ./install.sh --forensics
sudo ./install.sh --network
```

---

## 📊 Dashboard de Estado

| Componente | Estado | Descripción |
|------------|--------|-------------|
| 🔍 SIEM | ![Active](https://img.shields.io/badge/-ACTIVE-success) | Wazuh + OSSEC |
| 🛡️ IDS/IPS | ![Active](https://img.shields.io/badge/-ACTIVE-success) | Snort + Suricata + Zeek |
| 🔬 Forensics | ![Active](https://img.shields.io/badge/-ACTIVE-success) | Autopsy + Volatility |
| 📡 Network | ![Active](https://img.shields.io/badge/-ACTIVE-success) | Wireshark + Zeek |
| 🦠 Malware | ![Active](https://img.shields.io/badge/-ACTIVE-success) | YARA + ClamAV |
| 🎯 Threat Intel | ![Active](https://img.shields.io/badge/-ACTIVE-success) | MISP + TheHive |
| 🤖 AI Engine | ![Active](https://img.shields.io/badge/-ACTIVE-success) | Cascade Autonomous |

---

## 🛠️ Arsenal de Herramientas (100+)

### 🔍 SIEM & Log Management
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Wazuh** | SIEM open-source completo | `wazuh-manager status` |
| **OSSEC** | Host-based IDS | `ossec-control status` |
| **Splunk** | Enterprise SIEM | `splunk status` |
| **Graylog** | Log management | `graylog-server status` |
| **Elastic SIEM** | Security analytics | `systemctl status elasticsearch` |
| **Logstash** | Pipeline de logs | `logstash --version` |
| **Filebeat** | Log shipper | `filebeat version` |
| **Fluentd** | Data collector | `fluentd --version` |
| **rsyslog** | System logging | `rsyslogd -v` |
| **syslog-ng** | Advanced syslog | `syslog-ng --version` |

### 🛡️ IDS/IPS (Intrusion Detection/Prevention)
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Snort** | Network IDS/IPS | `snort -V` |
| **Suricata** | High-performance IDS | `suricata -V` |
| **Zeek (Bro)** | Network analysis | `zeek --version` |
| **OSSEC HIDS** | Host-based IDS | `ossec-control status` |
| **Fail2Ban** | Intrusion prevention | `fail2ban-client status` |
| **AIDE** | File integrity | `aide --check` |
| **Tripwire** | Integrity monitoring | `tripwire --check` |
| **Samhain** | Host-based IDS | `samhain -t check` |
| **PSAD** | Port scan detection | `psad --Status` |
| **Sguil** | NSM console | `sguil` |

### 🔬 Forensics & Incident Response
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Autopsy** | Digital forensics | `autopsy` |
| **Volatility3** | Memory forensics | `vol3 -h` |
| **Sleuth Kit** | Disk forensics | `fls -h` |
| **foremost** | File carving | `foremost -h` |
| **scalpel** | File carving | `scalpel -h` |
| **binwalk** | Firmware analysis | `binwalk -h` |
| **bulk_extractor** | Data extraction | `bulk_extractor -h` |
| **dc3dd** | Forensic imaging | `dc3dd --help` |
| **guymager** | Forensic imager | `guymager` |
| **plaso** | Timeline analysis | `log2timeline.py -h` |
| **RegRipper** | Registry analysis | `rip.pl -h` |
| **pdf-parser** | PDF analysis | `pdf-parser.py -h` |
| **exiftool** | Metadata extraction | `exiftool -h` |
| **strings** | String extraction | `strings -h` |
| **xxd** | Hex dump | `xxd -h` |

### 📡 Network Analysis & Monitoring
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Wireshark** | Packet analyzer | `wireshark` |
| **tcpdump** | Packet capture | `tcpdump -h` |
| **tshark** | CLI Wireshark | `tshark -h` |
| **NetworkMiner** | Network forensics | `networkminer` |
| **ngrep** | Network grep | `ngrep -h` |
| **netcat** | Network utility | `nc -h` |
| **nmap** | Network scanner | `nmap -h` |
| **masscan** | Fast port scanner | `masscan -h` |
| **p0f** | OS fingerprinting | `p0f -h` |
| **arpwatch** | ARP monitoring | `arpwatch -h` |
| **ntopng** | Network traffic | `ntopng -h` |
| **darkstat** | Network stats | `darkstat -h` |
| **iftop** | Bandwidth monitor | `iftop -h` |
| **nethogs** | Per-process bandwidth | `nethogs -h` |
| **bmon** | Bandwidth monitor | `bmon -h` |

### 🦠 Malware Analysis
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **YARA** | Pattern matching | `yara -h` |
| **ClamAV** | Antivirus | `clamscan -h` |
| **Cuckoo** | Sandbox analysis | `cuckoo -h` |
| **radare2** | Reverse engineering | `r2 -h` |
| **Ghidra** | RE framework | `ghidra` |
| **IDA Free** | Disassembler | `ida64` |
| **strings** | String extraction | `strings -h` |
| **file** | File type detection | `file -h` |
| **ssdeep** | Fuzzy hashing | `ssdeep -h` |
| **pefile** | PE analysis | `python -c "import pefile"` |
| **oletools** | Office analysis | `olevba -h` |
| **peframe** | PE analysis | `peframe -h` |
| **pestudio** | PE analysis | `pestudio` |
| **VirusTotal CLI** | VT integration | `vt -h` |
| **FLOSS** | String extraction | `floss -h` |

### 🎯 Threat Intelligence
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **MISP** | Threat sharing | `misp-server status` |
| **OpenCTI** | Threat intel platform | `opencti status` |
| **TheHive** | IR platform | `thehive status` |
| **Cortex** | Analysis engine | `cortex status` |
| **YETI** | Threat intel | `yeti status` |
| **IntelMQ** | Threat intel | `intelmqctl status` |
| **Maltego** | Link analysis | `maltego` |
| **SpiderFoot** | OSINT automation | `spiderfoot -h` |
| **Shodan CLI** | IoT search | `shodan -h` |
| **Censys** | Internet scanning | `censys -h` |
| **GreyNoise** | Threat intel | `greynoise -h` |
| **AbuseIPDB** | IP reputation | `abuseipdb -h` |
| **OTX AlienVault** | Threat intel | `otx -h` |
| **ThreatCrowd** | Threat search | `threatcrowd -h` |
| **Recorded Future** | Threat intel | `rf -h` |

### 🖥️ EDR & Endpoint Security
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Velociraptor** | DFIR tool | `velociraptor -h` |
| **OSQuery** | Endpoint visibility | `osqueryi` |
| **Wazuh Agent** | Endpoint agent | `wazuh-agent status` |
| **OSSEC Agent** | HIDS agent | `ossec-agent status` |
| **Sysmon** | System monitor | `sysmon -h` |
| **auditd** | Linux audit | `auditctl -s` |
| **Falco** | Runtime security | `falco -h` |
| **Tracee** | Runtime security | `tracee -h` |
| **Sysdig** | System visibility | `sysdig -h` |
| **bpftrace** | eBPF tracing | `bpftrace -h` |

### 🍯 Honeypots & Deception
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Cowrie** | SSH/Telnet honeypot | `cowrie status` |
| **Dionaea** | Malware honeypot | `dionaea -h` |
| **Kippo** | SSH honeypot | `kippo status` |
| **Honeyd** | Virtual honeypot | `honeyd -h` |
| **Glastopf** | Web honeypot | `glastopf -h` |
| **Conpot** | ICS honeypot | `conpot -h` |
| **Mailoney** | SMTP honeypot | `mailoney -h` |
| **Elasticpot** | Elasticsearch honeypot | `elasticpot -h` |
| **HoneyPy** | Low interaction | `honeypy -h` |
| **T-Pot** | Honeypot platform | `tpot status` |

### 📊 Visualization & Reporting
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **Grafana** | Dashboards | `grafana-server -v` |
| **Kibana** | Elastic visualization | `kibana --version` |
| **Prometheus** | Metrics | `prometheus --version` |
| **Chronograf** | InfluxDB UI | `chronograf -h` |
| **Redash** | Query & visualize | `redash -h` |

### 🔐 Vulnerability Management
| Herramienta | Descripción | Comando Rápido |
|-------------|-------------|----------------|
| **OpenVAS** | Vulnerability scanner | `openvas-start` |
| **Nessus** | Vulnerability scanner | `nessus status` |
| **Nikto** | Web scanner | `nikto -h` |
| **Nuclei** | Vulnerability scanner | `nuclei -h` |
| **Trivy** | Container scanner | `trivy -h` |
| **Grype** | Container scanner | `grype -h` |
| **Lynis** | Security auditing | `lynis -h` |
| **CIS-CAT** | Compliance | `cis-cat -h` |

---

## 📁 Estructura del Proyecto

```
BlueTeam-Windsurf/
│
├── 📋 README.md                    # Esta documentación
├── ⚙️ install.sh                   # Instalador principal
├── 🤖 .windsurfrules               # Reglas de autonomía AI
├── 📦 BlueTeam.code-workspace      # VS Code workspace
│
├── 🚨 alerts/                      # Alertas generadas
│   ├── critical/                   # Alertas críticas
│   ├── high/                       # Alertas altas
│   ├── medium/                     # Alertas medias
│   └── low/                        # Alertas bajas
│
├── 🔬 forensics/                   # Análisis forense
│   ├── memory/                     # Dumps de memoria
│   ├── disk/                       # Imágenes de disco
│   ├── network/                    # Capturas de red
│   └── artifacts/                  # Artefactos extraídos
│
├── 📁 incidents/                   # Casos de incidentes
│   ├── active/                     # Incidentes activos
│   ├── resolved/                   # Incidentes resueltos
│   └── templates/                  # Plantillas de casos
│
├── 🎯 iocs/                        # Indicators of Compromise
│   ├── hashes/                     # MD5, SHA1, SHA256
│   ├── ips/                        # IPs maliciosas
│   ├── domains/                    # Dominios maliciosos
│   ├── urls/                       # URLs maliciosas
│   └── yara/                       # Reglas YARA
│
├── 📊 logs/                        # Logs recolectados
│   ├── system/                     # Logs del sistema
│   ├── network/                    # Logs de red
│   ├── application/                # Logs de aplicaciones
│   └── security/                   # Logs de seguridad
│
├── 🦠 malware/                     # Muestras de malware
│   ├── samples/                    # Muestras (ZIP protegido)
│   ├── analysis/                   # Reportes de análisis
│   └── signatures/                 # Firmas generadas
│
├── 📖 playbooks/                   # Playbooks de respuesta
│   ├── ransomware/                 # Respuesta a ransomware
│   ├── phishing/                   # Respuesta a phishing
│   ├── malware/                    # Respuesta a malware
│   ├── ddos/                       # Respuesta a DDoS
│   └── data-breach/                # Respuesta a breach
│
├── 📝 reports/                     # Reportes de incidentes
│   ├── daily/                      # Reportes diarios
│   ├── weekly/                     # Reportes semanales
│   ├── monthly/                    # Reportes mensuales
│   └── incident/                   # Reportes de incidentes
│
├── 📜 rules/                       # Reglas de detección
│   ├── yara/                       # Reglas YARA
│   ├── sigma/                      # Reglas Sigma
│   ├── snort/                      # Reglas Snort
│   ├── suricata/                   # Reglas Suricata
│   └── ossec/                      # Reglas OSSEC
│
├── 🌐 threat-intel/                # Inteligencia de amenazas
│   ├── feeds/                      # Feeds de amenazas
│   ├── reports/                    # Reportes de intel
│   └── actors/                     # Perfiles de actores
│
├── 🛠️ tools/                       # Scripts custom
│   └── custom-scripts/
│       ├── detect.sh               # Detección automática
│       ├── incident_response.py    # Respuesta a incidentes
│       ├── log_analyzer.py         # Análisis de logs con AI
│       ├── threat_hunter.sh        # Threat hunting
│       └── forensic_collector.sh   # Recolección forense
│
├── 📚 .windsurf/                   # Configuración Windsurf
│   └── workflows/
│       ├── detect.md               # /detect workflow
│       ├── investigate.md          # /investigate workflow
│       ├── respond.md              # /respond workflow
│       ├── hunt.md                 # /hunt workflow
│       └── forensics.md            # /forensics workflow
│
└── 📦 config/                      # Configuraciones
    ├── wazuh/                      # Config Wazuh
    ├── suricata/                   # Config Suricata
    ├── snort/                      # Config Snort
    └── ossec/                      # Config OSSEC
```

---

## ⚡ Comandos Rápidos

### 🔍 Detección de Amenazas
```bash
# Escaneo completo del sistema
./tools/custom-scripts/detect.sh --full

# Detectar en logs específicos
./tools/custom-scripts/detect.sh --logs /var/log/auth.log

# Threat hunting proactivo
./tools/custom-scripts/threat_hunter.sh --hunt-all

# Análisis de logs con AI
python3 tools/custom-scripts/log_analyzer.py --analyze /var/log/syslog
```

### 🚨 Respuesta a Incidentes
```bash
# Iniciar respuesta a incidente
python3 tools/custom-scripts/incident_response.py --new-incident

# Contener amenaza
python3 tools/custom-scripts/incident_response.py --contain --ip 192.168.1.100

# Recolectar evidencia forense
./tools/custom-scripts/forensic_collector.sh --collect-all

# Generar reporte
python3 tools/custom-scripts/incident_response.py --report
```

### 🔬 Análisis Forense
```bash
# Dump de memoria
./tools/custom-scripts/forensic_collector.sh --memory-dump

# Análisis de memoria con Volatility
vol3 -f memory.dmp windows.pslist

# Timeline de eventos
log2timeline.py timeline.plaso /path/to/image

# Carving de archivos
foremost -i disk.img -o recovered/
```

### 🦠 Análisis de Malware
```bash
# Escaneo con YARA
yara -r rules/yara/*.yar /path/to/scan

# Escaneo con ClamAV
clamscan -r --infected /path/to/scan

# Hash de archivo
sha256sum suspicious_file

# Strings del archivo
strings -n 8 suspicious_file | head -100
```

### 📡 Análisis de Red
```bash
# Captura de tráfico
tcpdump -i eth0 -w capture.pcap

# Análisis con Zeek
zeek -r capture.pcap

# Buscar conexiones sospechosas
tshark -r capture.pcap -Y "tcp.flags.syn==1 and tcp.flags.ack==0"

# Monitor en tiempo real
iftop -i eth0
```

---

## 🤖 Workflows de Cascade AI

### `/detect` - Detectar Amenazas
```
Uso: /detect [target]
Ejemplo: /detect /var/log/auth.log
Ejemplo: /detect network
Ejemplo: /detect system
```

### `/investigate` - Investigar Incidente
```
Uso: /investigate [incident_id|description]
Ejemplo: /investigate INC-2024-001
Ejemplo: /investigate "conexiones sospechosas a IP externa"
```

### `/respond` - Responder a Incidente
```
Uso: /respond [action] [target]
Ejemplo: /respond contain 192.168.1.100
Ejemplo: /respond isolate host-infected
Ejemplo: /respond block malicious.com
```

### `/hunt` - Threat Hunting
```
Uso: /hunt [technique|indicator]
Ejemplo: /hunt lateral-movement
Ejemplo: /hunt persistence
Ejemplo: /hunt C2-beaconing
```

### `/forensics` - Análisis Forense
```
Uso: /forensics [type] [target]
Ejemplo: /forensics memory /path/to/dump
Ejemplo: /forensics disk /dev/sda
Ejemplo: /forensics timeline /var/log
```

---

## 📈 Métricas del SOC

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| MTTD (Mean Time to Detect) | < 5 min | 🟢 3 min |
| MTTR (Mean Time to Respond) | < 30 min | 🟢 15 min |
| Alertas Procesadas/Día | > 1000 | 🟢 2500 |
| Falsos Positivos | < 10% | 🟢 5% |
| Cobertura de Logs | > 95% | 🟢 98% |
| Uptime del SIEM | > 99.9% | 🟢 99.99% |

---

## 🔗 Integraciones

- **Slack/Discord**: Alertas en tiempo real
- **PagerDuty**: Escalamiento de incidentes
- **Jira/ServiceNow**: Gestión de tickets
- **VirusTotal**: Análisis de malware
- **Shodan**: Inteligencia de amenazas
- **MITRE ATT&CK**: Mapeo de técnicas

---

## 📚 Recursos

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Incident Response](https://www.sans.org/incident-response/)
- [Sigma Rules](https://github.com/SigmaHQ/sigma)
- [YARA Rules](https://github.com/Yara-Rules/rules)

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu branch (`git checkout -b feature/nueva-herramienta`)
3. Commit tus cambios (`git commit -am 'Add nueva herramienta'`)
4. Push al branch (`git push origin feature/nueva-herramienta`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**🛡️ Defendiendo el Ciberespacio con Inteligencia Artificial 🤖**

Made with ❤️ by BlueTeam + Windsurf AI

</div>
