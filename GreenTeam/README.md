<p align="center">
  <img src="https://img.shields.io/badge/🛡️-GREEN_TEAM-00FF00?style=for-the-badge&labelColor=000000" alt="Green Team"/>
</p>

<h1 align="center">
  🟢 GREEN TEAM - DevSecOps Workspace
</h1>

<p align="center">
  <strong>🔐 Shift-Left Security | 🤖 AI-Powered | ⚡ Automated Pipeline</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Security-DevSecOps-00FF00?style=flat-square&logo=shield&logoColor=white" alt="DevSecOps"/>
  <img src="https://img.shields.io/badge/AI-Windsurf-0066FF?style=flat-square&logo=openai&logoColor=white" alt="Windsurf AI"/>
  <img src="https://img.shields.io/badge/SAST-Enabled-brightgreen?style=flat-square" alt="SAST"/>
  <img src="https://img.shields.io/badge/DAST-Enabled-brightgreen?style=flat-square" alt="DAST"/>
  <img src="https://img.shields.io/badge/SCA-Enabled-brightgreen?style=flat-square" alt="SCA"/>
  <img src="https://img.shields.io/badge/Container-Secured-brightgreen?style=flat-square&logo=docker" alt="Container"/>
  <img src="https://img.shields.io/badge/IaC-Scanned-brightgreen?style=flat-square&logo=terraform" alt="IaC"/>
  <img src="https://img.shields.io/badge/Secrets-Protected-brightgreen?style=flat-square&logo=keybase" alt="Secrets"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OWASP-Top_10-red?style=flat-square" alt="OWASP"/>
  <img src="https://img.shields.io/badge/CWE-Compliant-orange?style=flat-square" alt="CWE"/>
  <img src="https://img.shields.io/badge/CVE-Monitored-yellow?style=flat-square" alt="CVE"/>
  <img src="https://img.shields.io/badge/NIST-Framework-blue?style=flat-square" alt="NIST"/>
  <img src="https://img.shields.io/badge/ISO_27001-Aligned-purple?style=flat-square" alt="ISO"/>
</p>

---

## 📋 Tabla de Contenidos

- [🎯 Objetivo](#-objetivo)
- [🏗️ Arquitectura](#️-arquitectura)
- [🔧 Herramientas](#-herramientas)
- [🚀 Pipeline de Seguridad](#-pipeline-de-seguridad)
- [📦 Instalación](#-instalación)
- [🎮 Comandos Rápidos](#-comandos-rápidos)
- [📊 Workflows](#-workflows)
- [🤖 Integración Windsurf AI](#-integración-windsurf-ai)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔗 Integración CI/CD](#-integración-cicd)

---

## 🎯 Objetivo

> **Integrar seguridad en cada fase del ciclo de desarrollo (Shift-Left Security)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🛡️ SHIFT-LEFT SECURITY                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   📝 PLAN    →    💻 CODE    →    🔨 BUILD    →    🧪 TEST    →    🚀 DEPLOY │
│      │              │               │               │               │       │
│      ▼              ▼               ▼               ▼               ▼       │
│   ┌──────┐     ┌──────┐        ┌──────┐        ┌──────┐        ┌──────┐    │
│   │Threat│     │ SAST │        │ SCA  │        │ DAST │        │ WAF  │    │
│   │Model │     │Secrets│       │Container│     │ API  │        │Monitor│   │
│   └──────┘     └──────┘        └──────┘        └──────┘        └──────┘    │
│                                                                             │
│   ◀────────────────── SEGURIDAD CONTINUA ──────────────────▶               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Arquitectura

```
                          ┌─────────────────────────────────────┐
                          │        🤖 WINDSURF AI               │
                          │    Análisis Inteligente de Código   │
                          └──────────────┬──────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │   📊 SAST       │  │   🌐 DAST       │  │   📦 SCA        │
          │   Static        │  │   Dynamic       │  │   Software      │
          │   Analysis      │  │   Analysis      │  │   Composition   │
          ├─────────────────┤  ├─────────────────┤  ├─────────────────┤
          │ • Semgrep       │  │ • OWASP ZAP     │  │ • Snyk          │
          │ • SonarQube     │  │ • Nuclei        │  │ • Dependabot    │
          │ • Bandit        │  │ • Nikto         │  │ • OWASP DC      │
          │ • ESLint Sec    │  │ • Burp Suite    │  │ • npm audit     │
          └─────────────────┘  └─────────────────┘  └─────────────────┘
                    │                    │                    │
                    └────────────────────┼────────────────────┘
                                         │
          ┌──────────────────────────────┼──────────────────────────────┐
          │                              │                              │
          ▼                              ▼                              ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│   🔑 SECRETS    │            │   🐳 CONTAINER  │            │   🏗️ IaC        │
│   Detection     │            │   Security      │            │   Security      │
├─────────────────┤            ├─────────────────┤            ├─────────────────┤
│ • Gitleaks      │            │ • Trivy         │            │ • Checkov       │
│ • TruffleHog    │            │ • Grype         │            │ • tfsec         │
│ • detect-secrets│            │ • Clair         │            │ • KICS          │
│ • git-secrets   │            │ • Falco         │            │ • Terrascan     │
└─────────────────┘            └─────────────────┘            └─────────────────┘
                                         │
                                         ▼
                          ┌─────────────────────────────────────┐
                          │      📈 SECURITY DASHBOARD          │
                          │   Métricas | Reportes | Alertas     │
                          └─────────────────────────────────────┘
```

---

## 🔧 Herramientas

### 📊 SAST (Static Application Security Testing)

| Herramienta | Descripción | Lenguajes |
|-------------|-------------|-----------|
| **Semgrep** | Análisis estático rápido y extensible | Multi-lenguaje |
| **SonarQube** | Plataforma de calidad de código | 25+ lenguajes |
| **Bandit** | Análisis de seguridad para Python | Python |
| **ESLint Security** | Reglas de seguridad para JavaScript | JS/TS |
| **Brakeman** | Scanner para Ruby on Rails | Ruby |
| **SpotBugs** | Análisis de bytecode Java | Java |

### 🌐 DAST (Dynamic Application Security Testing)

| Herramienta | Descripción | Tipo |
|-------------|-------------|------|
| **OWASP ZAP** | Proxy de seguridad web | Web Scanner |
| **Nuclei** | Scanner de vulnerabilidades rápido | Template-based |
| **Nikto** | Scanner de servidores web | Web Server |
| **Burp Suite** | Suite de testing de seguridad | Proxy/Scanner |
| **Arachni** | Framework de seguridad web | Web Framework |

### 📦 SCA (Software Composition Analysis)

| Herramienta | Descripción | Ecosistema |
|-------------|-------------|------------|
| **Snyk** | Análisis de dependencias | Multi-plataforma |
| **Dependabot** | Actualizaciones automáticas | GitHub |
| **OWASP Dependency-Check** | Detección de CVEs | Multi-lenguaje |
| **npm audit** | Auditoría de paquetes npm | Node.js |
| **Safety** | Verificación de dependencias Python | Python |

### 🔑 Detección de Secrets

| Herramienta | Descripción | Integración |
|-------------|-------------|-------------|
| **Gitleaks** | Detección de secrets en git | CI/CD |
| **TruffleHog** | Búsqueda de credenciales | Git History |
| **detect-secrets** | Prevención de secrets | Pre-commit |
| **git-secrets** | Hooks de prevención | Git Hooks |

### 🐳 Seguridad de Containers

| Herramienta | Descripción | Función |
|-------------|-------------|---------|
| **Trivy** | Scanner de vulnerabilidades | Images/IaC |
| **Grype** | Análisis de vulnerabilidades | Container Images |
| **Clair** | Análisis estático de containers | Registry Integration |
| **Falco** | Runtime security | Kubernetes |
| **Anchore** | Análisis de imágenes | Policy Engine |

### 🏗️ Infrastructure as Code (IaC)

| Herramienta | Descripción | Plataformas |
|-------------|-------------|-------------|
| **Checkov** | Scanner de IaC | Terraform/K8s/ARM |
| **tfsec** | Análisis de Terraform | Terraform |
| **KICS** | Keeping IaC Secure | Multi-IaC |
| **Terrascan** | Compliance as Code | Multi-cloud |

---

## 🚀 Pipeline de Seguridad

```yaml
┌──────────────────────────────────────────────────────────────────────────────┐
│                        🔄 SECURITY PIPELINE                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │  CODE   │───▶│  SCAN   │───▶│  BUILD  │───▶│  TEST   │───▶│ DEPLOY  │   │
│  │ COMMIT  │    │ SECRETS │    │  IMAGE  │    │  DAST   │    │ MONITOR │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│       │              │              │              │              │         │
│       ▼              ▼              ▼              ▼              ▼         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │Pre-commit│   │Gitleaks │    │ Trivy   │    │OWASP ZAP│    │ Falco   │   │
│  │  Hooks  │    │TruffleHog│   │ Grype   │    │ Nuclei  │    │ Alerts  │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│       │              │              │              │              │         │
│       ▼              ▼              ▼              ▼              ▼         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ SAST    │    │ SCA     │    │Container│    │  API    │    │ SIEM    │   │
│  │Semgrep  │    │ Snyk    │    │ Scan    │    │Security │    │ Logs    │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════   │
│                         📊 SECURITY GATES                                    │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                              │
│  ✅ Critical: 0    ⚠️ High: ≤5    🔶 Medium: ≤20    ℹ️ Low: Unlimited       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Instalación

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/your-org/greenteam-windsurf.git
cd greenteam-windsurf

# Ejecutar instalador
chmod +x install.sh
./install.sh
```

### Instalación Manual

```bash
# SAST Tools
pip install semgrep bandit
npm install -g eslint eslint-plugin-security

# DAST Tools
sudo apt install zaproxy nikto
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# SCA Tools
npm install -g snyk
pip install safety

# Secret Scanners
brew install gitleaks trufflehog
pip install detect-secrets

# Container Security
brew install trivy
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s

# IaC Security
pip install checkov
brew install tfsec
```

---

## 🎮 Comandos Rápidos

### Workflows Disponibles

| Comando | Descripción |
|---------|-------------|
| `/scan-code` | Escaneo completo de código fuente |
| `/check-deps` | Verificar dependencias y vulnerabilidades |
| `/scan-container` | Escanear imagen de container |
| `/full-pipeline` | Ejecutar pipeline completo de seguridad |
| `/scan-secrets` | Buscar secrets expuestos |
| `/scan-iac` | Escanear Infrastructure as Code |

### Scripts Disponibles

```bash
# Escaneo completo de código
./tools/custom-scripts/secure_scan.sh <directorio>

# Verificar dependencias
python tools/custom-scripts/dependency_check.py

# Buscar secrets
./tools/custom-scripts/secret_scanner.sh <directorio>

# Escanear containers
./tools/custom-scripts/container_scan.sh <imagen>

# Pipeline completo
python tools/custom-scripts/pipeline_security.py
```

---

## 📊 Workflows

### `/scan-code` - Escaneo de Código

```
┌────────────────────────────────────────────┐
│           📊 SCAN-CODE WORKFLOW            │
├────────────────────────────────────────────┤
│                                            │
│  1️⃣  Detectar lenguajes del proyecto       │
│           │                                │
│           ▼                                │
│  2️⃣  Ejecutar Semgrep (multi-lenguaje)     │
│           │                                │
│           ▼                                │
│  3️⃣  Ejecutar scanner específico           │
│      • Python → Bandit                     │
│      • JavaScript → ESLint Security        │
│      • Java → SpotBugs                     │
│           │                                │
│           ▼                                │
│  4️⃣  Generar reporte consolidado           │
│           │                                │
│           ▼                                │
│  5️⃣  Sugerir fixes automáticos             │
│                                            │
└────────────────────────────────────────────┘
```

### `/full-pipeline` - Pipeline Completo

```
┌────────────────────────────────────────────────────────────────┐
│                  🔄 FULL PIPELINE WORKFLOW                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ SECRETS  │──▶│   SAST   │──▶│   SCA    │──▶│   IaC    │   │
│  │  SCAN    │   │   SCAN   │   │   SCAN   │   │   SCAN   │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│       │              │              │              │          │
│       ▼              ▼              ▼              ▼          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │Container │──▶│   DAST   │──▶│   API    │──▶│  REPORT  │   │
│  │   SCAN   │   │   SCAN   │   │   SCAN   │   │ GENERATE │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│                                                                │
│  ════════════════════════════════════════════════════════════ │
│                     📈 METRICS & GATES                         │
│  ════════════════════════════════════════════════════════════ │
│                                                                │
│  Total Vulns: XX | Critical: X | High: X | Medium: X | Low: X │
│                                                                │
│  ✅ PASS / ❌ FAIL                                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Integración Windsurf AI

### Reglas Automáticas

```yaml
# .windsurfrules
triggers:
  on_code_receive:
    - action: auto_scan
      tools: [semgrep, bandit, eslint-security]
    
  on_vulnerability_found:
    - action: suggest_fix
      priority: critical_first
    
  on_commit:
    - action: run_pipeline
      stages: [secrets, sast, sca]
```

### Capacidades AI

| Función | Descripción |
|---------|-------------|
| **Auto-Scan** | Escaneo automático al recibir código |
| **Fix Suggestion** | Sugerencias de corrección inteligentes |
| **Pattern Learning** | Aprendizaje de patrones de vulnerabilidades |
| **Risk Assessment** | Evaluación de riesgo contextual |
| **Code Review** | Revisión de seguridad asistida por AI |

---

## 📁 Estructura del Proyecto

```
GreenTeam-Windsurf/
│
├── 📄 README.md                    # Este archivo
├── 📄 memoria.md                   # Documentación detallada
├── 🔧 install.sh                   # Script de instalación
├── 📄 .windsurfrules               # Reglas de Windsurf AI
│
├── 📁 scans/                       # Resultados de escaneos
│   ├── sast/                       # Resultados SAST
│   ├── dast/                       # Resultados DAST
│   ├── sca/                        # Resultados SCA
│   └── reports/                    # Reportes consolidados
│
├── 📁 vulnerabilities/             # Vulnerabilidades encontradas
│   ├── critical/                   # Críticas
│   ├── high/                       # Altas
│   ├── medium/                     # Medias
│   └── low/                        # Bajas
│
├── 📁 fixes/                       # Fixes sugeridos
│   ├── templates/                  # Templates de corrección
│   └── automated/                  # Fixes automáticos
│
├── 📁 policies/                    # Políticas de seguridad
│   ├── security-gates.yaml         # Gates de seguridad
│   ├── compliance/                 # Políticas de compliance
│   └── standards/                  # Estándares (OWASP, CWE)
│
├── 📁 pipelines/                   # Configuraciones CI/CD
│   ├── github-actions/             # GitHub Actions
│   ├── gitlab-ci/                  # GitLab CI
│   ├── jenkins/                    # Jenkins
│   └── azure-devops/               # Azure DevOps
│
├── 📁 containers/                  # Seguridad de containers
│   ├── dockerfiles/                # Dockerfiles seguros
│   ├── policies/                   # Políticas de containers
│   └── scans/                      # Resultados de scans
│
├── 📁 iac/                         # Infrastructure as Code
│   ├── terraform/                  # Módulos Terraform
│   ├── kubernetes/                 # Manifiestos K8s
│   └── policies/                   # Políticas IaC
│
├── 📁 secrets/                     # Gestión de secrets
│   ├── .gitleaks.toml              # Config Gitleaks
│   ├── .secrets.baseline           # Baseline detect-secrets
│   └── vault/                      # Integración Vault
│
├── 📁 tools/                       # Scripts y herramientas
│   └── custom-scripts/             # Scripts personalizados
│       ├── secure_scan.sh          # Escaneo completo
│       ├── dependency_check.py     # Verificar dependencias
│       ├── secret_scanner.sh       # Buscar secrets
│       ├── container_scan.sh       # Escanear containers
│       └── pipeline_security.py    # Pipeline de seguridad
│
└── 📁 .windsurf/                   # Configuración Windsurf
    ├── workflows/                  # Workflows
    │   ├── scan-code.md
    │   ├── check-deps.md
    │   ├── scan-container.md
    │   └── full-pipeline.md
    └── skills/                     # Skills
        ├── vulnerability-analysis.md
        ├── secure-coding.md
        └── compliance-check.md
```

---

## 🔗 Integración CI/CD

### GitHub Actions

```yaml
name: Security Pipeline
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Secret Scan
        uses: gitleaks/gitleaks-action@v2
        
      - name: SAST Scan
        uses: returntocorp/semgrep-action@v1
        
      - name: SCA Scan
        uses: snyk/actions/node@master
        
      - name: Container Scan
        uses: aquasecurity/trivy-action@master
```

### GitLab CI

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
```

---

## 📈 Métricas y KPIs

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| **MTTR** (Mean Time To Remediate) | < 24h | - |
| **Vulnerabilidades Críticas** | 0 | - |
| **Cobertura de Escaneo** | 100% | - |
| **False Positive Rate** | < 5% | - |
| **Security Debt** | Decreciente | - |

---

## 🏆 Compliance

<p align="center">
  <img src="https://img.shields.io/badge/OWASP-Top_10_2021-red?style=for-the-badge" alt="OWASP"/>
  <img src="https://img.shields.io/badge/CWE-Top_25-orange?style=for-the-badge" alt="CWE"/>
  <img src="https://img.shields.io/badge/SANS-Top_25-yellow?style=for-the-badge" alt="SANS"/>
  <img src="https://img.shields.io/badge/PCI_DSS-Compliant-blue?style=for-the-badge" alt="PCI"/>
  <img src="https://img.shields.io/badge/HIPAA-Ready-purple?style=for-the-badge" alt="HIPAA"/>
  <img src="https://img.shields.io/badge/SOC2-Type_II-green?style=for-the-badge" alt="SOC2"/>
</p>

---

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-herramienta`)
3. Commit cambios (`git commit -am 'Add: nueva herramienta de seguridad'`)
4. Push a la rama (`git push origin feature/nueva-herramienta`)
5. Crear Pull Request

---

## 📞 Soporte

| Canal | Contacto |
|-------|----------|
| 📧 Email | security@greenteam.dev |
| 💬 Slack | #green-team-devsecops |
| 📝 Issues | GitHub Issues |

---

<p align="center">
  <strong>🛡️ Seguridad desde el primer commit hasta producción 🛡️</strong>
</p>

<p align="center">
  <sub>Built with ❤️ by GREEN TEAM | Powered by Windsurf AI</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made_with-Security_First-00FF00?style=for-the-badge" alt="Security First"/>
</p>
