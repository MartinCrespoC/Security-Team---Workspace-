# 📚 MEMORIA DE CONSTRUCCIÓN - GREEN TEAM DevSecOps Workspace

<p align="center">
  <img src="https://img.shields.io/badge/🛡️-GREEN_TEAM-00FF00?style=for-the-badge&labelColor=000000" alt="Green Team"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge" alt="Status"/>
</p>

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#-resumen-ejecutivo)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Estructura de Directorios](#-estructura-de-directorios)
4. [Componentes Principales](#-componentes-principales)
5. [Herramientas Integradas](#-herramientas-integradas)
6. [Workflows Disponibles](#-workflows-disponibles)
7. [Skills de Windsurf AI](#-skills-de-windsurf-ai)
8. [Scripts Personalizados](#-scripts-personalizados)
9. [Configuración de Reglas](#-configuración-de-reglas)
10. [Integración CI/CD](#-integración-cicd)
11. [Guía de Instalación](#-guía-de-instalación)
12. [Uso y Operación](#-uso-y-operación)
13. [Métricas y KPIs](#-métricas-y-kpis)
14. [Troubleshooting](#-troubleshooting)
15. [Roadmap](#-roadmap)

---

## 🎯 Resumen Ejecutivo

### Objetivo
Crear un workspace completo de DevSecOps que integre seguridad en cada fase del ciclo de desarrollo (Shift-Left Security), potenciado por Windsurf AI para análisis automático y sugerencias inteligentes.

### Alcance
- **SAST**: Análisis estático de código fuente
- **DAST**: Análisis dinámico de aplicaciones
- **SCA**: Análisis de composición de software
- **Secret Detection**: Detección de credenciales expuestas
- **Container Security**: Seguridad de contenedores Docker
- **IaC Security**: Seguridad de Infrastructure as Code
- **API Security**: Seguridad de APIs

### Beneficios
| Beneficio | Descripción |
|-----------|-------------|
| 🚀 Automatización | Escaneos automáticos en cada commit |
| 🔍 Detección Temprana | Vulnerabilidades detectadas en desarrollo |
| 💡 Fixes Inteligentes | Sugerencias de corrección con AI |
| 📊 Visibilidad | Dashboards y reportes consolidados |
| 🔄 Integración | Compatible con CI/CD existente |
| 💜 Purple Team | Colaboración Red/Blue Team |

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GREEN TEAM WORKSPACE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        🤖 WINDSURF AI LAYER                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │   Rules     │  │  Workflows  │  │   Skills    │  │  Triggers   │  │   │
│  │  │.windsurfrules│ │  /scan-*    │  │ vuln-analysis│ │  on_commit  │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      🔧 SECURITY TOOLS LAYER                         │   │
│  │                                                                       │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │   │
│  │  │  SAST   │ │  DAST   │ │   SCA   │ │ SECRETS │ │CONTAINER│        │   │
│  │  │─────────│ │─────────│ │─────────│ │─────────│ │─────────│        │   │
│  │  │Semgrep  │ │OWASP ZAP│ │ Snyk    │ │Gitleaks │ │ Trivy   │        │   │
│  │  │Bandit   │ │Nuclei   │ │Safety   │ │TruffleHog│ │ Grype   │        │   │
│  │  │ESLint   │ │Nikto    │ │npm audit│ │detect-sec│ │Hadolint │        │   │
│  │  │Gosec    │ │         │ │         │ │         │ │ Dockle  │        │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │   │
│  │                                                                       │   │
│  │  ┌─────────┐ ┌─────────┐                                             │   │
│  │  │   IaC   │ │   API   │                                             │   │
│  │  │─────────│ │─────────│                                             │   │
│  │  │Checkov  │ │Newman   │                                             │   │
│  │  │tfsec    │ │HTTPie   │                                             │   │
│  │  │KICS     │ │jwt-cli  │                                             │   │
│  │  └─────────┘ └─────────┘                                             │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      📊 OUTPUT & REPORTING                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │   Scans     │  │Vulnerabilities│ │   Fixes    │  │  Reports    │  │   │
│  │  │   /scans/   │  │/vulnerabilities│ │  /fixes/   │  │  /reports/  │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  CODE   │───▶│ TRIGGER │───▶│  SCAN   │───▶│ ANALYZE │───▶│ REPORT  │
│ COMMIT  │    │ DETECT  │    │ EXECUTE │    │ RESULTS │    │ GENERATE│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Git    │    │Windsurf │    │ Tools   │    │   AI    │    │  JSON   │
│  Hook   │    │ Rules   │    │ Layer   │    │ Engine  │    │   MD    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## 📁 Estructura de Directorios

```
GreenTeam-Windsurf/
│
├── 📄 README.md                          # Documentación principal
├── 📄 memoria.md                         # Este archivo - documentación detallada
├── 🔧 install.sh                         # Script de instalación completo
├── 📄 .windsurfrules                     # Reglas de Windsurf AI
│
├── 📁 scans/                             # Resultados de escaneos
│   ├── sast/                             # Resultados SAST (Semgrep, Bandit, etc.)
│   ├── dast/                             # Resultados DAST (ZAP, Nuclei, etc.)
│   ├── sca/                              # Resultados SCA (Snyk, Safety, etc.)
│   ├── secrets/                          # Resultados de detección de secrets
│   ├── containers/                       # Resultados de escaneo de containers
│   ├── iac/                              # Resultados de escaneo IaC
│   ├── pipeline/                         # Resultados de pipeline completo
│   └── reports/                          # Reportes consolidados
│
├── 📁 vulnerabilities/                   # Vulnerabilidades encontradas
│   ├── critical/                         # Vulnerabilidades críticas
│   ├── high/                             # Vulnerabilidades altas
│   ├── medium/                           # Vulnerabilidades medias
│   └── low/                              # Vulnerabilidades bajas
│
├── 📁 fixes/                             # Fixes sugeridos
│   ├── templates/                        # Templates de corrección
│   └── automated/                        # Fixes automáticos generados
│
├── 📁 policies/                          # Políticas de seguridad
│   ├── security-gates.yaml               # Configuración de gates
│   ├── compliance/                       # Políticas de compliance
│   │   ├── owasp-top10.yaml
│   │   ├── pci-dss.yaml
│   │   ├── hipaa.yaml
│   │   └── soc2.yaml
│   └── standards/                        # Estándares de seguridad
│       ├── cwe-top25.yaml
│       └── sans-top25.yaml
│
├── 📁 pipelines/                         # Configuraciones CI/CD
│   ├── github-actions/                   # GitHub Actions workflows
│   │   └── security-pipeline.yml
│   ├── gitlab-ci/                        # GitLab CI configuration
│   │   └── .gitlab-ci.yml
│   ├── jenkins/                          # Jenkins pipelines
│   │   └── Jenkinsfile
│   └── azure-devops/                     # Azure DevOps pipelines
│       └── azure-pipelines.yml
│
├── 📁 containers/                        # Seguridad de containers
│   ├── dockerfiles/                      # Dockerfiles seguros de ejemplo
│   │   ├── python-secure.dockerfile
│   │   ├── node-secure.dockerfile
│   │   └── go-secure.dockerfile
│   ├── policies/                         # Políticas de containers
│   │   └── container-policy.yaml
│   └── scans/                            # Resultados de scans de containers
│
├── 📁 iac/                               # Infrastructure as Code
│   ├── terraform/                        # Módulos Terraform seguros
│   │   └── secure-vpc/
│   ├── kubernetes/                       # Manifiestos K8s seguros
│   │   └── secure-deployment.yaml
│   └── policies/                         # Políticas IaC
│       └── iac-policy.yaml
│
├── 📁 secrets/                           # Gestión de secrets
│   ├── .gitleaks.toml                    # Configuración Gitleaks
│   ├── .secrets.baseline                 # Baseline detect-secrets
│   └── vault/                            # Integración con Vault
│       └── vault-config.hcl
│
├── 📁 tools/                             # Scripts y herramientas
│   └── custom-scripts/                   # Scripts personalizados
│       ├── secure_scan.sh                # Escaneo completo de código
│       ├── dependency_check.py           # Verificar dependencias
│       ├── secret_scanner.sh             # Buscar secrets
│       ├── container_scan.sh             # Escanear containers
│       └── pipeline_security.py          # Pipeline de seguridad
│
└── 📁 .windsurf/                         # Configuración Windsurf
    ├── workflows/                        # Workflows disponibles
    │   ├── scan-code.md                  # /scan-code
    │   ├── check-deps.md                 # /check-deps
    │   ├── scan-container.md             # /scan-container
    │   ├── scan-secrets.md               # /scan-secrets
    │   ├── scan-iac.md                   # /scan-iac
    │   └── full-pipeline.md              # /full-pipeline
    └── skills/                           # Skills de AI
        ├── vulnerability-analysis.md     # Análisis de vulnerabilidades
        ├── secure-coding.md              # Guía de código seguro
        ├── compliance-check.md           # Verificación de compliance
        └── purple-team-collaboration.md  # Colaboración Purple Team
```

---

## 🧩 Componentes Principales

### 1. README.md
**Propósito:** Documentación principal del proyecto con información visual y accesible.

**Contenido:**
- Badges de estado y tecnologías
- Diagrama de arquitectura ASCII
- Tabla de herramientas por categoría
- Pipeline de seguridad visual
- Instrucciones de instalación
- Comandos rápidos
- Estructura del proyecto
- Integración CI/CD
- Métricas y KPIs
- Información de compliance

### 2. install.sh
**Propósito:** Script de instalación automatizada de todas las herramientas de seguridad.

**Características:**
- Detección automática de sistema operativo (Linux, macOS)
- Instalación por categorías (SAST, DAST, SCA, etc.)
- Verificación de herramientas existentes
- Logging de instalación
- Menú interactivo
- Soporte para instalación parcial
- Configuración post-instalación

**Herramientas instaladas:**
| Categoría | Herramientas |
|-----------|--------------|
| SAST | Semgrep, Bandit, ESLint Security, Gosec, Brakeman, SpotBugs, SonarScanner |
| DAST | OWASP ZAP, Nuclei, Nikto, httpx, ffuf |
| SCA | Snyk, Safety, pip-audit, npm audit, RetireJS, OWASP Dependency-Check |
| Secrets | Gitleaks, TruffleHog, detect-secrets, git-secrets |
| Container | Trivy, Grype, Syft, Hadolint, Dockle |
| IaC | Checkov, tfsec, KICS, Terrascan, Terraform |
| API | Newman, HTTPie, jwt-cli, Inso |

### 3. .windsurfrules
**Propósito:** Configuración de reglas automáticas para Windsurf AI.

**Triggers configurados:**
| Trigger | Acción |
|---------|--------|
| `on_code_receive` | Escaneo automático de seguridad |
| `on_vulnerability_found` | Sugerencia de fix |
| `on_commit` | Pipeline de seguridad |
| `on_dependency_change` | Escaneo SCA |
| `on_container_config` | Escaneo de containers |
| `on_iac_change` | Escaneo de IaC |

**Patrones de vulnerabilidades:**
- SQL Injection (CWE-89)
- XSS (CWE-79)
- Command Injection (CWE-78)
- Path Traversal (CWE-22)
- Hardcoded Secrets (CWE-798)
- Insecure Deserialization (CWE-502)
- SSRF (CWE-918)
- Weak Cryptography (CWE-327)

---

## 🔧 Herramientas Integradas

### SAST (Static Application Security Testing)

| Herramienta | Lenguajes | Descripción | Comando |
|-------------|-----------|-------------|---------|
| **Semgrep** | Multi | Scanner SAST rápido y extensible | `semgrep scan --config auto` |
| **Bandit** | Python | Análisis de seguridad para Python | `bandit -r . -f json` |
| **ESLint Security** | JS/TS | Reglas de seguridad para JavaScript | `eslint --plugin security` |
| **Gosec** | Go | Security checker para Go | `gosec ./...` |
| **Brakeman** | Ruby | Scanner para Ruby on Rails | `brakeman -f json` |
| **SpotBugs** | Java | Análisis de bytecode Java | `spotbugs -textui` |

### DAST (Dynamic Application Security Testing)

| Herramienta | Tipo | Descripción | Comando |
|-------------|------|-------------|---------|
| **OWASP ZAP** | Web Scanner | Proxy de seguridad web | `zap-cli quick-scan` |
| **Nuclei** | Template-based | Scanner de vulnerabilidades rápido | `nuclei -u <target>` |
| **Nikto** | Web Server | Scanner de servidores web | `nikto -h <target>` |
| **httpx** | HTTP Toolkit | Herramienta HTTP versátil | `httpx -u <target>` |
| **ffuf** | Fuzzer | Web fuzzer rápido | `ffuf -u <target>/FUZZ` |

### SCA (Software Composition Analysis)

| Herramienta | Ecosistema | Descripción | Comando |
|-------------|------------|-------------|---------|
| **Snyk** | Multi | Análisis de dependencias | `snyk test` |
| **Safety** | Python | Verificación de dependencias Python | `safety check` |
| **pip-audit** | Python | Auditoría de paquetes pip | `pip-audit` |
| **npm audit** | Node.js | Auditoría de paquetes npm | `npm audit` |
| **RetireJS** | JavaScript | Scanner de librerías JS | `retire` |
| **OWASP DC** | Multi | Detección de CVEs | `dependency-check.sh` |

### Secret Detection

| Herramienta | Descripción | Comando |
|-------------|-------------|---------|
| **Gitleaks** | Detección de secrets en git | `gitleaks detect` |
| **TruffleHog** | Búsqueda de credenciales | `trufflehog filesystem` |
| **detect-secrets** | Prevención de secrets | `detect-secrets scan` |
| **git-secrets** | Hooks de prevención | `git secrets --scan` |

### Container Security

| Herramienta | Función | Comando |
|-------------|---------|---------|
| **Trivy** | Vulnerabilidades | `trivy image <image>` |
| **Grype** | Vulnerabilidades | `grype <image>` |
| **Syft** | SBOM | `syft <image>` |
| **Hadolint** | Dockerfile Linting | `hadolint Dockerfile` |
| **Dockle** | Best Practices | `dockle <image>` |

### IaC Security

| Herramienta | Plataformas | Comando |
|-------------|-------------|---------|
| **Checkov** | Terraform/K8s/ARM | `checkov -d .` |
| **tfsec** | Terraform | `tfsec .` |
| **KICS** | Multi-IaC | `kics scan -p .` |
| **Terrascan** | Multi-cloud | `terrascan scan` |

---

## 🔄 Workflows Disponibles

### /scan-code
**Descripción:** Escaneo completo de código fuente usando SAST.

**Pasos:**
1. Detectar lenguajes del proyecto
2. Ejecutar Semgrep (multi-lenguaje)
3. Ejecutar scanner específico por lenguaje
4. Generar reporte consolidado
5. Sugerir fixes automáticos

**Uso:**
```
/scan-code
```

### /check-deps
**Descripción:** Verificar dependencias por vulnerabilidades conocidas.

**Pasos:**
1. Detectar ecosistemas de dependencias
2. Ejecutar Safety/pip-audit (Python)
3. Ejecutar npm audit (Node.js)
4. Ejecutar Snyk (multi-ecosistema)
5. Generar reporte de vulnerabilidades

**Uso:**
```
/check-deps
```

### /scan-container
**Descripción:** Escanear imagen Docker o Dockerfile.

**Pasos:**
1. Identificar target (imagen o Dockerfile)
2. Ejecutar Hadolint (Dockerfile linting)
3. Ejecutar Trivy (vulnerabilidades)
4. Ejecutar Grype (análisis adicional)
5. Ejecutar Dockle (best practices)
6. Generar SBOM con Syft

**Uso:**
```
/scan-container nginx:latest
/scan-container ./Dockerfile
```

### /scan-secrets
**Descripción:** Buscar secrets y credenciales expuestas.

**Pasos:**
1. Ejecutar Gitleaks
2. Ejecutar TruffleHog
3. Ejecutar detect-secrets
4. Buscar patrones personalizados
5. Generar reporte

**Uso:**
```
/scan-secrets
```

### /scan-iac
**Descripción:** Escanear Infrastructure as Code.

**Pasos:**
1. Detectar tipos de IaC
2. Ejecutar Checkov
3. Ejecutar tfsec (Terraform)
4. Ejecutar KICS
5. Generar reporte de compliance

**Uso:**
```
/scan-iac
```

### /full-pipeline
**Descripción:** Ejecutar pipeline completo de seguridad.

**Stages:**
1. Secret Detection
2. SAST Scan
3. SCA Scan
4. IaC Security
5. Container Security
6. Report Generation

**Uso:**
```
/full-pipeline
/full-pipeline --image nginx:latest
/full-pipeline --stages secrets sast sca
```

---

## 🧠 Skills de Windsurf AI

### vulnerability-analysis
**Propósito:** Análisis profundo de vulnerabilidades y sugerencia de fixes.

**Capacidades:**
- Detección de vulnerabilidades por categoría
- Clasificación de severidad
- Mapeo a CWE/OWASP
- Generación de código corregido
- Referencias a documentación

### secure-coding
**Propósito:** Guía para desarrollo de código seguro.

**Contenido:**
- Principios de código seguro
- Checklists por lenguaje
- Patrones de diseño seguros
- Ejemplos de código seguro vs inseguro

### compliance-check
**Propósito:** Verificación de compliance con estándares.

**Frameworks soportados:**
- OWASP Top 10 (2021)
- CWE Top 25 (2023)
- PCI DSS v4.0
- HIPAA
- SOC 2 Type II

### purple-team-collaboration
**Propósito:** Facilitar colaboración entre Red Team y Blue/Green Team.

**Funcionalidades:**
- Formato de reportes Red Team → Green Team
- Formato de respuestas Green Team → Red Team
- Ejercicios Purple Team
- Métricas de colaboración
- Integración con MITRE ATT&CK

---

## 📜 Scripts Personalizados

### secure_scan.sh
**Ubicación:** `tools/custom-scripts/secure_scan.sh`

**Funcionalidad:**
- Detectar lenguajes del proyecto
- Ejecutar Semgrep, Bandit, ESLint, Gosec según corresponda
- Generar reportes en JSON y texto
- Crear resumen consolidado

**Uso:**
```bash
./tools/custom-scripts/secure_scan.sh <directorio>
```

### dependency_check.py
**Ubicación:** `tools/custom-scripts/dependency_check.py`

**Funcionalidad:**
- Detectar ecosistemas de dependencias
- Ejecutar Safety, pip-audit, npm audit, Snyk
- Clasificar vulnerabilidades por severidad
- Generar reportes JSON y Markdown

**Uso:**
```bash
python tools/custom-scripts/dependency_check.py <directorio>
```

### secret_scanner.sh
**Ubicación:** `tools/custom-scripts/secret_scanner.sh`

**Funcionalidad:**
- Ejecutar Gitleaks, TruffleHog, detect-secrets
- Buscar patrones personalizados
- Generar reportes consolidados
- Evaluar security gate

**Uso:**
```bash
./tools/custom-scripts/secret_scanner.sh <directorio>
```

### container_scan.sh
**Ubicación:** `tools/custom-scripts/container_scan.sh`

**Funcionalidad:**
- Escanear imágenes Docker con Trivy, Grype
- Analizar Dockerfiles con Hadolint
- Verificar best practices con Dockle
- Generar SBOM con Syft

**Uso:**
```bash
./tools/custom-scripts/container_scan.sh -i <imagen>
./tools/custom-scripts/container_scan.sh -f <Dockerfile>
```

### pipeline_security.py
**Ubicación:** `tools/custom-scripts/pipeline_security.py`

**Funcionalidad:**
- Orquestar todas las etapas del pipeline
- Ejecutar escaneos en paralelo cuando sea posible
- Evaluar security gates
- Generar reportes ejecutivos

**Uso:**
```bash
python tools/custom-scripts/pipeline_security.py
python tools/custom-scripts/pipeline_security.py --stages secrets sast
python tools/custom-scripts/pipeline_security.py --image nginx:latest
```

---

## ⚙️ Configuración de Reglas

### Security Gates

```yaml
security_gates:
  block_on:
    - critical_vulnerabilities: 0
    - high_vulnerabilities: 5
    - secrets_detected: 0
    - critical_misconfigurations: 0
  
  warn_on:
    - medium_vulnerabilities: 20
    - outdated_dependencies: 10
    - low_vulnerabilities: unlimited
```

### Excepciones

```yaml
exceptions:
  allowed_paths:
    - "test/**"
    - "tests/**"
    - "spec/**"
    - "**/test_*.py"
    - "**/*_test.go"
    - "**/*.test.js"
  
  false_positive_handling:
    - document_reason
    - require_approval
    - set_expiration
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

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Security Pipeline') {
            steps {
                sh 'python tools/custom-scripts/pipeline_security.py'
            }
        }
    }
}
```

---

## 📦 Guía de Instalación

### Requisitos Previos

- **Sistema Operativo:** Linux (Debian/Ubuntu, RHEL/Fedora, Arch) o macOS
- **Python:** 3.8+
- **Node.js:** 16+
- **Go:** 1.19+
- **Docker:** 20+ (opcional, para escaneo de containers)
- **Git:** 2.30+

### Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/your-org/greenteam-windsurf.git
cd greenteam-windsurf

# Dar permisos de ejecución
chmod +x install.sh
chmod +x tools/custom-scripts/*.sh

# Ejecutar instalación completa
./install.sh --full

# O usar menú interactivo
./install.sh
```

### Instalación por Categoría

```bash
./install.sh --sast        # Solo herramientas SAST
./install.sh --dast        # Solo herramientas DAST
./install.sh --sca         # Solo herramientas SCA
./install.sh --secrets     # Solo detección de secrets
./install.sh --containers  # Solo seguridad de containers
./install.sh --iac         # Solo seguridad IaC
./install.sh --api         # Solo herramientas API
```

### Verificación

```bash
./install.sh --verify
```

### Post-Instalación

```bash
# Recargar PATH
source ~/.bashrc  # o ~/.zshrc

# Configurar Snyk (requiere cuenta)
snyk auth

# Actualizar templates de Nuclei
nuclei -update-templates

# Actualizar base de datos de Trivy
trivy image --download-db-only
```

---

## 🎮 Uso y Operación

### Uso Básico

```bash
# Escaneo rápido de código
./tools/custom-scripts/secure_scan.sh .

# Verificar dependencias
python tools/custom-scripts/dependency_check.py .

# Buscar secrets
./tools/custom-scripts/secret_scanner.sh .

# Pipeline completo
python tools/custom-scripts/pipeline_security.py
```

### Uso con Windsurf AI

1. **Compartir código** → Análisis automático de seguridad
2. **Usar workflows** → `/scan-code`, `/check-deps`, etc.
3. **Recibir sugerencias** → Fixes automáticos con explicación

### Interpretación de Resultados

```
✅ PASSED  - Sin vulnerabilidades críticas, cumple security gates
⚠️ WARNING - Vulnerabilidades encontradas pero dentro de umbrales
❌ FAILED  - Vulnerabilidades críticas o secrets expuestos
```

---

## 📊 Métricas y KPIs

### Métricas de Seguridad

| Métrica | Objetivo | Descripción |
|---------|----------|-------------|
| MTTR | < 24h | Mean Time To Remediate |
| Vulnerabilidades Críticas | 0 | En producción |
| Cobertura de Escaneo | 100% | Código escaneado |
| False Positive Rate | < 5% | Precisión de detección |
| Security Debt | Decreciente | Vulnerabilidades pendientes |

### Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Dashboard                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Vulnerabilities          Detection Coverage                     │
│  ┌────────────────┐       ┌────────────────┐                    │
│  │ 🔴 Critical: 0 │       │ ████████░░ 85% │                    │
│  │ 🟠 High: 3     │       └────────────────┘                    │
│  │ 🟡 Medium: 12  │                                              │
│  │ 🔵 Low: 28     │       Response Time                          │
│  └────────────────┘       ┌────────────────┐                    │
│                           │ Avg: 4.2 hours │                    │
│  Scans Today: 47          │ Best: 15 min   │                    │
│  Issues Fixed: 8          │ Worst: 24 hours│                    │
│                           └────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Problemas Comunes

| Problema | Solución |
|----------|----------|
| Herramienta no encontrada | Verificar PATH, ejecutar `source ~/.bashrc` |
| Permisos denegados | Ejecutar con `sudo` o verificar permisos de archivos |
| Timeout en escaneos | Aumentar timeout o escanear por partes |
| Memoria insuficiente | Reducir paralelismo o aumentar memoria |
| False positives | Agregar a excepciones en `.windsurfrules` |

### Logs

```bash
# Ver log de instalación
cat install.log

# Ver reportes de escaneo
ls -la scans/*/
```

### Soporte

- 📧 Email: security@greenteam.dev
- 💬 Slack: #green-team-devsecops
- 📝 Issues: GitHub Issues

---

## 🗺️ Roadmap

### v1.1 (Q3 2024)
- [ ] Integración con Jira para tracking de vulnerabilidades
- [ ] Dashboard web interactivo
- [ ] Soporte para más lenguajes (Rust, Kotlin)
- [ ] Integración con Slack/Teams para notificaciones

### v1.2 (Q4 2024)
- [ ] Machine Learning para reducir false positives
- [ ] Auto-remediation para vulnerabilidades comunes
- [ ] Integración con SIEM (Splunk, ELK)
- [ ] API REST para integración externa

### v2.0 (Q1 2025)
- [ ] Plataforma SaaS
- [ ] Multi-tenant support
- [ ] Advanced analytics y trending
- [ ] Compliance automation

---

## 📝 Changelog

### v1.0.0 (2024-05-04)
- ✅ Estructura inicial del workspace
- ✅ README.md con documentación completa
- ✅ install.sh con instalación automatizada
- ✅ .windsurfrules con triggers automáticos
- ✅ Scripts personalizados (secure_scan, dependency_check, etc.)
- ✅ Workflows de Windsurf (/scan-code, /check-deps, etc.)
- ✅ Skills de AI (vulnerability-analysis, secure-coding, etc.)
- ✅ Integración Purple Team
- ✅ Memoria de construcción

---

<p align="center">
  <strong>🛡️ GREEN TEAM - Seguridad desde el primer commit 🛡️</strong>
</p>

<p align="center">
  <sub>Construido con ❤️ para la comunidad DevSecOps</sub>
</p>
