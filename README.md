<p align="center">
  <img src="https://img.shields.io/badge/Security-Teams-red?style=for-the-badge&logo=shield&logoColor=white" alt="Security Teams"/>
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/Multi--Agent-Orchestration-purple?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Multi-Agent"/>
</p>

<h1 align="center">🛡️ Security Team Workspace</h1>

<p align="center">
  <strong>El primer framework de ciberseguridad con 7 equipos de agentes IA especializados que trabajan en paralelo con contextos aislados</strong>
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
  <a href="#-características">Características</a> •
  <a href="#-equipos">Equipos</a> •
  <a href="#-instalación">Instalación</a> •
  <a href="#-uso">Uso</a> •
  <a href="#-reportes">Reportes</a> •
  <a href="#-compatibilidad">Compatibilidad</a>
</p>

---

## 🎯 ¿Qué es Security Team Workspace?

**Security Team Workspace** es un framework revolucionario que orquesta **7 equipos de agentes IA especializados** en ciberseguridad. Cada equipo opera con su propio contexto aislado, pero pueden comunicarse y colaborar en tiempo real para ejecutar operaciones de seguridad complejas.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🛡️ SECURITY TEAM ORCHESTRATOR                        │
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
│  ✅ Contextos Aislados  ✅ Comunicación Inter-Equipos  ✅ Reportes Unificados │
└─────────────────────────────────────────────────────────────────────────────┘
```

## ✨ Características

### 🚀 Multi-Agente Paralelo
- **7 equipos especializados** trabajando simultáneamente
- **Contextos completamente aislados** por proyecto y equipo
- **Comunicación segura** entre equipos via `secteam share`
- **Orquestación inteligente** que asigna tareas al equipo correcto

### 🎯 Capacidades Ofensivas (RedTeam)
- Reconocimiento automatizado (subdominios, puertos, servicios)
- Explotación de vulnerabilidades (web, network, API)
- Post-explotación y movimiento lateral
- Generación de payloads y bypasses

### 🛡️ Capacidades Defensivas (BlueTeam)
- Detección de amenazas en tiempo real
- Análisis forense de incidentes
- Threat hunting proactivo
- Integración con SIEM/IDS/IPS

### 🔄 Validación Continua (PurpleTeam)
- Simulación de ataques MITRE ATT&CK
- Validación de detecciones
- Gap analysis automatizado
- Ejercicios de Purple Team

### 📊 Mega Reportes Detallados
- **Hallazgos por equipo** con severidad y evidencia
- **CVEs y CWEs** identificados
- **Exploits y payloads** utilizados
- **Accesos conseguidos** y credenciales
- **Secrets expuestos** encontrados
- **Recomendaciones de remediación**
- **Timeline de actividades**

---

## 🎨 Equipos

<table>
<tr>
<td width="50%">

### 🔴 RedTeam - Offensive Security
**Rol:** Romper todo lo que se pueda romper

**Capacidades:**
- 🔍 Reconnaissance & OSINT
- 🌐 Web Application Attacks
- 🔓 Exploitation & Post-Exploitation
- 🎭 Social Engineering
- 🔑 Credential Attacks
- 🚀 Privilege Escalation

**Herramientas:**
`metasploit` `nmap` `burpsuite` `sqlmap` `nuclei` `ffuf` `gobuster` `hydra` `john` `hashcat`

</td>
<td width="50%">

### 🔵 BlueTeam - Defensive Security
**Rol:** Proteger todo lo que se pueda proteger

**Capacidades:**
- 🔔 Threat Detection
- 🚨 Incident Response
- 🔬 Digital Forensics
- 📊 Log Analysis
- 🕵️ Threat Hunting
- 📡 Network Monitoring

**Herramientas:**
`wazuh` `suricata` `zeek` `volatility` `yara` `osquery` `velociraptor` `splunk` `elastic`

</td>
</tr>
<tr>
<td width="50%">

### 🟣 PurpleTeam - Security Validation
**Rol:** Validar ataques y detecciones

**Capacidades:**
- ⚔️ Attack Simulation
- ✅ Detection Validation
- 📉 Gap Analysis
- 🗺️ MITRE ATT&CK Mapping
- 🔄 Continuous Validation

**Herramientas:**
`caldera` `atomic-red-team` `dettect` `attack-navigator` `vectr` `infection-monkey`

</td>
<td width="50%">

### 🟢 GreenTeam - DevSecOps
**Rol:** Seguridad en el desarrollo

**Capacidades:**
- 🔍 SAST (Static Analysis)
- 🌐 DAST (Dynamic Analysis)
- 📦 SCA (Dependency Check)
- 🐳 Container Security
- 🏗️ IaC Security
- 🔐 Secret Detection

**Herramientas:**
`semgrep` `trivy` `gitleaks` `checkov` `snyk` `zap` `nuclei` `grype` `hadolint`

</td>
</tr>
<tr>
<td width="50%">

### ⚪ WhiteTeam - GRC
**Rol:** Governance, Risk & Compliance

**Capacidades:**
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
**Rol:** Diseño seguro desde el inicio

**Capacidades:**
- 🎯 Threat Modeling (STRIDE)
- 🏛️ Architecture Review
- 📋 Security Requirements
- 🔒 Zero Trust Design
- 📐 Secure Patterns

**Herramientas:**
`pytm` `threat-dragon` `diagrams` `draw.io` `plantuml`

</td>
</tr>
<tr>
<td colspan="2">

### 🟠 OrangeTeam - Security Awareness
**Rol:** El factor humano

**Capacidades:**
- 🎣 Phishing Simulation
- 📚 Security Training
- 📊 Awareness Metrics
- 🎭 Social Engineering Tests
- 📈 Campaign Analytics

**Herramientas:**
`gophish` `king-phisher` `set` `beef` `evilginx2`

</td>
</tr>
</table>

---

## 🚀 Instalación

### Requisitos Previos
- Linux (Kali Linux recomendado)
- Python 3.8+
- Docker & Docker Compose
- Git

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/MartinCrespoC/Security-Team---Workspace-.git
cd Security-Team---Workspace-

# Instalación completa (requiere sudo)
sudo ./install.sh --full

# O instalación interactiva
sudo ./install.sh
```

### Post-Instalación

⚠️ **IMPORTANTE:** Después de la instalación, configura los archivos `.env` necesarios:

```bash
# Copiar templates de configuración
cp RedTeam/.env.example RedTeam/.env
cp BlueTeam/.env.example BlueTeam/.env
cp OrangeTeam/.env.example OrangeTeam/.env

# Editar con tus API keys y configuraciones
nano RedTeam/.env
```

**Variables de entorno comunes:**
| Variable | Descripción | Equipos |
|----------|-------------|---------|
| `SHODAN_API_KEY` | API key de Shodan | RedTeam |
| `VIRUSTOTAL_API_KEY` | API key de VirusTotal | BlueTeam |
| `SLACK_WEBHOOK` | Webhook para notificaciones | Todos |
| `SMTP_SERVER` | Servidor SMTP para phishing | OrangeTeam |

---

## 📋 Uso

### Comandos del Orquestador

```bash
# Ver estado del workspace
secteam status

# Crear nuevo proyecto con contextos aislados
secteam new proyecto-cliente-xyz

# Activar contexto de equipo
secteam red      # 🔴 Red Team
secteam blue     # 🔵 Blue Team
secteam purple   # 🟣 Purple Team
secteam green    # 🟢 Green Team
secteam white    # ⚪ White Team
secteam yellow   # 🟡 Yellow Team
secteam orange   # 🟠 Orange Team

# Compartir hallazgos entre equipos
secteam share BlueTeam vulnerability-report.md

# Listar proyectos
secteam list

# Generar mega reporte
secteam report proyecto-cliente-xyz
```

### Ejemplo: Operación Completa de Seguridad

```bash
# 1. Crear proyecto
secteam new operacion-aurora

# 2. RedTeam: Reconocimiento y explotación
secteam red
# La IA ejecutará: nmap, nuclei, sqlmap, etc.

# 3. BlueTeam: Analizar detecciones
secteam blue
# La IA analizará logs y alertas generadas

# 4. PurpleTeam: Validar brechas
secteam purple
# La IA mapeará a MITRE ATT&CK

# 5. Generar mega reporte
secteam report operacion-aurora --full
```

---

## 📊 Sistema de Reportes

El framework genera **Mega Reportes** detallados con toda la información de la operación:

### Estructura del Reporte

```
📁 reports/
└── 📁 operacion-aurora-20240504/
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

### Contenido del Mega Reporte

| Sección | Contenido |
|---------|-----------|
| **Executive Summary** | Resumen ejecutivo para directivos |
| **Hallazgos** | Vulnerabilidades por severidad (Critical/High/Medium/Low) |
| **CVEs Identificados** | Lista de CVEs con descripción y CVSS |
| **CWEs Mapeados** | Debilidades categorizadas por CWE |
| **Exploits Utilizados** | Código y payloads usados |
| **Accesos Conseguidos** | Sistemas comprometidos y nivel de acceso |
| **Credenciales** | Hashes, passwords crackeados, API keys |
| **Secrets Expuestos** | Tokens, keys, certificados encontrados |
| **Timeline** | Cronología de la operación |
| **Equipo Responsable** | Qué equipo descubrió cada hallazgo |
| **Remediación** | Fixes recomendados con prioridad |

---

## 🤖 Compatibilidad con IDEs

Este workspace funciona con **cualquier IDE con asistente IA**:

| IDE/Asistente | Archivo de Configuración | Estado |
|---------------|-------------------------|--------|
| **Windsurf** | `.windsurfrules` | ✅ |
| **Cursor** | `.cursorrules` | ✅ |
| **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ |
| **Cline/Claude Dev** | `.clinerules` | ✅ |
| **Gemini** | `.gemini` | ✅ |
| **Claude** | `CLAUDE.md` | ✅ |

### Uso con IA

Simplemente abre el workspace en tu IDE y solicita:

```
"Haz un pentest completo de example.com"
"Analiza estos logs por actividad maliciosa"
"Escanea el código por vulnerabilidades"
"Crea un threat model de la aplicación"
"Genera un reporte de cumplimiento ISO 27001"
```

La IA identificará automáticamente qué equipo(s) deben actuar y ejecutará las herramientas apropiadas.

---

## 📁 Estructura del Proyecto

```
Security-Team---Workspace-/
│
├── 🔴 RedTeam/                    # Herramientas ofensivas
│   ├── tools/
│   ├── scripts/
│   ├── wordlists/
│   └── .env.example
│
├── 🔵 BlueTeam/                   # Herramientas defensivas
│   ├── rules/
│   ├── playbooks/
│   ├── iocs/
│   └── .env.example
│
├── 🟣 PurpleTeam/                 # Validación
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
├── 🟡 YellowTeam/                 # Arquitectura
│   ├── threat-models/
│   ├── architectures/
│   └── requirements/
│
├── 🟠 OrangeTeam/                 # Awareness
│   ├── campaigns/
│   ├── training/
│   └── templates/
│
├── 📁 .contexts/                  # Configuración de contextos
│   └── config.json
│
├── 📁 .projects/                  # Proyectos (contextos aislados)
│
├── 📁 .shared/                    # Hallazgos compartidos
│
├── 📁 .windsurf/workflows/        # Workflows de automatización
│
├── 📁 reports/                    # Mega reportes generados
│
├── 🔧 secteam                     # CLI Orquestador
├── 🔧 install.sh                  # Instalador unificado
├── 📄 .windsurfrules              # Config Windsurf
├── 📄 .cursorrules                # Config Cursor
├── 📄 .clinerules                 # Config Cline
├── 📄 .gemini                     # Config Gemini
├── 📄 CLAUDE.md                   # Config Claude
├── 📄 LICENSE                     # Licencia
└── 📄 README.md                   # Este archivo
```

---

## ⚠️ Disclaimer

Este framework está diseñado **exclusivamente para uso autorizado** en:
- Pruebas de penetración autorizadas
- Evaluaciones de seguridad contratadas
- Investigación de seguridad ética
- Entornos de laboratorio y CTFs

**El uso no autorizado de estas herramientas es ilegal y está estrictamente prohibido.**

---

## 📜 Licencia

Este proyecto está bajo la licencia **Security Research License**. Ver [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, lee las guías de contribución antes de enviar un PR.

---

## 👨‍💻 Autor

**Martin Crespo**

---

<p align="center">
  <strong>🛡️ Break Everything. Protect Everything. Report Everything. 🛡️</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge" alt="Made with love"/>
</p>
