<![CDATA[# 🟡 YELLOW TEAM - Memoria de Construcción

<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗ █████╗                  ║
║   ████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗██║██╔══██╗                 ║
║   ██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝██║███████║                 ║
║   ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗██║██╔══██║                 ║
║   ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║██║██║  ██║                 ║
║   ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝                 ║
║                                                                               ║
║          🟡 YELLOW TEAM - SECURITY ARCHITECTURE WORKSPACE 🟡                  ║
║                                                                               ║
║                    Documentación Completa de Construcción                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

</div>

---

## 📋 Índice

1. [Visión General](#-visión-general)
2. [Arquitectura del Workspace](#-arquitectura-del-workspace)
3. [Estructura de Directorios](#-estructura-de-directorios)
4. [Archivos de Configuración](#-archivos-de-configuración)
5. [Scripts Personalizados](#-scripts-personalizados)
6. [Workflows](#-workflows)
7. [Skills](#-skills)
8. [Integración con Purple Team](#-integración-con-purple-team)
9. [Guía de Uso](#-guía-de-uso)
10. [Mantenimiento](#-mantenimiento)

---

## 🎯 Visión General

### Propósito
El **Yellow Team Workspace** es un entorno completo para **Arquitectura de Seguridad** y **Threat Modeling**, diseñado para trabajar con Windsurf AI.

### Objetivos
| Objetivo | Descripción |
|----------|-------------|
| **Diseño Seguro** | Crear arquitecturas resilientes desde el inicio |
| **Threat Modeling** | Identificar y mitigar amenazas sistemáticamente |
| **Zero Trust** | Implementar arquitecturas de confianza cero |
| **Compliance** | Alinear con estándares y regulaciones |
| **Automatización** | Scripts y herramientas para acelerar el trabajo |

### Metodologías Soportadas
- **STRIDE** - Threat modeling por categorías
- **PASTA** - Process for Attack Simulation and Threat Analysis
- **Attack Trees** - Modelado de vectores de ataque
- **SABSA** - Security Architecture Framework
- **TOGAF** - Enterprise Architecture con seguridad
- **NIST CSF** - Cybersecurity Framework
- **Zero Trust** - Arquitectura de confianza cero

---

## 🏗️ Arquitectura del Workspace

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        YELLOW TEAM WORKSPACE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │   WINDSURF AI   │  │    SCRIPTS      │  │   TEMPLATES     │            │
│  │   + Rules       │  │    Python/Bash  │  │   MD/JSON       │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                    │                      │
│           └────────────────────┼────────────────────┘                      │
│                                │                                           │
│                    ┌───────────▼───────────┐                               │
│                    │     CORE ENGINE       │                               │
│                    │  - Threat Modeling    │                               │
│                    │  - Architecture Review│                               │
│                    │  - Zero Trust Check   │                               │
│                    │  - Attack Trees       │                               │
│                    │  - Requirements Gen   │                               │
│                    └───────────┬───────────┘                               │
│                                │                                           │
│           ┌────────────────────┼────────────────────┐                      │
│           │                    │                    │                      │
│  ┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼─────────┐            │
│  │  THREAT MODELS  │  │    REVIEWS      │  │  REQUIREMENTS   │            │
│  │  - STRIDE       │  │  - Security     │  │  - Specs        │            │
│  │  - PASTA        │  │  - Architecture │  │  - Controls     │            │
│  │  - Attack Trees │  │  - Compliance   │  │  - Compliance   │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        OUTPUT FORMATS                               │   │
│  │  📄 Markdown  │  📊 JSON  │  📈 Mermaid Diagrams  │  📋 Reports    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Directorios

```
YellowTeam-Windsurf/
│
├── 📄 README.md                          # Documentación principal
├── 📄 memoria.md                         # Este archivo
├── 📄 YellowTeam.code-workspace          # Configuración VS Code/Windsurf
├── 📄 install.sh                         # Script de instalación
├── 📄 .windsurfrules                     # Reglas para Windsurf AI
├── 📄 .gitignore                         # Archivos ignorados por Git
├── 📄 requirements.txt                   # Dependencias Python
├── 📄 mkdocs.yml                         # Configuración MkDocs
│
├── 📁 architectures/                     # Diagramas de arquitectura
│   ├── templates/                        # Plantillas
│   └── examples/                         # Ejemplos
│
├── 📁 threat-models/                     # Modelos de amenazas
│   ├── templates/                        # Plantillas STRIDE/PASTA
│   └── completed/                        # Modelos completados
│
├── 📁 requirements/                      # Requisitos de seguridad
│   ├── templates/                        # Plantillas
│   └── projects/                         # Por proyecto
│
├── 📁 patterns/                          # Patrones de diseño seguro
│   ├── authentication/                   # Autenticación
│   ├── authorization/                    # Autorización
│   ├── encryption/                       # Cifrado
│   └── network/                          # Red
│
├── 📁 frameworks/                        # Frameworks de referencia
│   ├── sabsa/                            # SABSA
│   ├── togaf/                            # TOGAF
│   ├── nist/                             # NIST CSF
│   └── zero-trust/                       # Zero Trust
│
├── 📁 reviews/                           # Revisiones de arquitectura
│   ├── templates/                        # Plantillas
│   └── completed/                        # Completadas
│
├── 📁 tools/                             # Herramientas
│   └── custom-scripts/                   # Scripts personalizados
│       ├── threat_model.py               # Generador de threat models
│       ├── architecture_review.py        # Revisor de arquitectura
│       ├── zero_trust_check.sh           # Validador Zero Trust
│       ├── attack_tree.py                # Generador de attack trees
│       └── security_requirements.py      # Generador de requisitos
│
├── 📁 templates/                         # Plantillas generales
│   ├── threat-models/                    # Threat model templates
│   ├── architectures/                    # Architecture templates
│   └── requirements/                     # Requirements templates
│
├── 📁 reports/                           # Reportes generados
│
├── 📁 docs/                              # Documentación MkDocs
│
└── 📁 .windsurf/                         # Configuración Windsurf
    ├── workflows/                        # Workflows automatizados
    │   ├── threat-model.md               # /threat-model
    │   ├── review-arch.md                # /review-arch
    │   └── zero-trust.md                 # /zero-trust
    └── skills/                           # Skills para AI
        ├── threat-analysis.md            # Análisis de amenazas
        ├── secure-design.md              # Diseño seguro
        └── compliance-check.md           # Verificación compliance
```

---

## ⚙️ Archivos de Configuración

### YellowTeam.code-workspace

**Propósito:** Configuración del workspace para VS Code/Windsurf

**Características:**
| Característica | Descripción |
|----------------|-------------|
| **Tema Yellow** | Colores amarillos en la interfaz |
| **Extensiones** | Recomendaciones de extensiones |
| **Tasks** | Tareas predefinidas para scripts |
| **Launch** | Configuraciones de debug |
| **Settings** | Configuración del editor |

**Tareas disponibles:**
```
🔍 Generate Threat Model
🏗️ Architecture Review
🛡️ Zero Trust Validation
🌳 Generate Attack Tree
📋 Generate Security Requirements
📊 Full Security Analysis
🚀 Install Dependencies
```

### .windsurfrules

**Propósito:** Reglas de comportamiento para Windsurf AI

**Comportamientos automáticos:**
1. **Al recibir arquitectura** → Analizar amenazas con STRIDE
2. **Nuevo sistema** → Crear threat model automáticamente
3. **Revisión de diseño** → Validar contra Zero Trust

**Formatos de salida:**
- STRIDE Analysis estructurado
- Data Flow Diagrams con Mermaid
- Attack Trees con notación estándar
- Requisitos con formato SHALL/SHOULD/MAY

### install.sh

**Propósito:** Instalador completo del ambiente

**Componentes instalados:**
| Categoría | Herramientas |
|-----------|--------------|
| **Sistema** | git, curl, wget, jq, graphviz, plantuml, java |
| **Python** | Virtual environment + dependencias |
| **Node.js** | mermaid-cli, markdownlint-cli |
| **Docs** | MkDocs con tema Material |

**Funciones principales:**
```bash
detect_package_manager()    # Detecta apt/dnf/yum/pacman/brew
install_system_deps()       # Instala dependencias del sistema
setup_python_env()          # Crea venv e instala paquetes
install_node_tools()        # Instala herramientas Node.js
create_directory_structure() # Crea estructura de directorios
create_templates()          # Genera plantillas iniciales
```

---

## 🔧 Scripts Personalizados

### threat_model.py

**Propósito:** Generador interactivo de threat models

**Características:**
- Modo interactivo guiado
- Análisis STRIDE completo
- Generación de DFD con Mermaid
- Cálculo automático de riesgo
- Exportación a Markdown y JSON

**Uso:**
```bash
# Modo interactivo
python tools/custom-scripts/threat_model.py --interactive

# Generar plantilla
python tools/custom-scripts/threat_model.py template
```

**Estructura de datos:**
```python
class ThreatModel:
    name: str
    description: str
    components: List[Dict]
    data_flows: List[Dict]
    trust_boundaries: List[Dict]
    threats: List[Dict]
    mitigations: List[Dict]
```

### architecture_review.py

**Propósito:** Herramienta de revisión de seguridad de arquitecturas

**Checklist incluido:**
- 🔐 Authentication (8 checks)
- 🛡️ Authorization (7 checks)
- 🔒 Data Protection (8 checks)
- 🌐 Network Security (8 checks)
- 📊 Logging & Monitoring (8 checks)
- 💻 Application Security (8 checks)
- 🏗️ Infrastructure (8 checks)
- 📋 Compliance (7 checks)

**Uso:**
```bash
# Modo interactivo
python tools/custom-scripts/architecture_review.py --interactive

# Ver checklist
python tools/custom-scripts/architecture_review.py checklist
```

### zero_trust_check.sh

**Propósito:** Validación de principios Zero Trust

**Áreas evaluadas:**
| Área | Verificaciones |
|------|----------------|
| **Identity** | MFA, SSH config, IdP |
| **Devices** | EDR, OSQuery, encryption, firewall |
| **Network** | Segmentation, TLS, VPN, DNS |
| **Applications** | Containers, secrets, WAF |
| **Data** | Encryption tools, permissions |
| **Visibility** | Logging, monitoring, SIEM |

**Uso:**
```bash
bash tools/custom-scripts/zero_trust_check.sh
```

**Output:**
- Score de madurez Zero Trust (%)
- Rating: Traditional/Initial/Advanced/Optimal
- Recomendaciones por área

### attack_tree.py

**Propósito:** Generador de árboles de ataque

**Características:**
- Construcción interactiva de nodos
- Soporte para nodos AND/OR
- Cálculo de riesgo por path
- Generación de diagramas Mermaid
- Análisis de rutas de ataque

**Uso:**
```bash
# Modo interactivo
python tools/custom-scripts/attack_tree.py --interactive

# Ver ejemplos
python tools/custom-scripts/attack_tree.py examples
```

### security_requirements.py

**Propósito:** Generador de especificaciones de requisitos de seguridad

**Catálogo incluido:**
| Categoría | Requisitos |
|-----------|------------|
| AUTH | 6 requisitos de autenticación |
| AUTHZ | 5 requisitos de autorización |
| CRYPTO | 5 requisitos de criptografía |
| DATA | 5 requisitos de protección de datos |
| LOG | 5 requisitos de logging |
| NET | 5 requisitos de red |
| APP | 6 requisitos de aplicación |
| CONF | 4 requisitos de configuración |

**Uso:**
```bash
# Modo interactivo
python tools/custom-scripts/security_requirements.py --interactive

# Generar todos los requisitos
python tools/custom-scripts/security_requirements.py generate --project "Mi Sistema" --all

# Ver catálogo
python tools/custom-scripts/security_requirements.py catalog
```

---

## 🔄 Workflows

### /threat-model

**Archivo:** `.windsurf/workflows/threat-model.md`

**Pasos:**
1. Gather System Information
2. Create Data Flow Diagram
3. Perform STRIDE Analysis
4. Document Threats
5. Generate Report
6. Review and Validate

**Comando turbo:**
```bash
python tools/custom-scripts/threat_model.py --interactive
```

### /review-arch

**Archivo:** `.windsurf/workflows/review-arch.md`

**Pasos:**
1. Understand the System
2. Identify Components
3. Security Checklist Evaluation
4. Document Findings
5. Generate Report
6. Risk Assessment
7. Recommendations

**Comando turbo:**
```bash
python tools/custom-scripts/architecture_review.py --interactive
```

### /zero-trust

**Archivo:** `.windsurf/workflows/zero-trust.md`

**Pasos:**
1. Identity Verification
2. Device Verification
3. Network Verification
4. Application Verification
5. Data Verification
6. Visibility & Analytics
7. Run Validation Script
8. Generate Report

**Comando turbo:**
```bash
bash tools/custom-scripts/zero_trust_check.sh
```

---

## 🧠 Skills

### threat-analysis.md

**Capacidades:**
- STRIDE Analysis automático
- Identificación de vectores de ataque
- Mapeo a vulnerabilidades (OWASP, CWE)
- Evaluación de riesgo

**Comandos:**
- `/analyze-threats [system]`
- `/stride [component]`
- `/attack-vectors [system]`
- `/risk-assess [threat]`

### secure-design.md

**Capacidades:**
- Security by Design principles
- Patrones de arquitectura segura
- Alineación con frameworks
- Integración de compliance

**Comandos:**
- `/design-secure [system]`
- `/secure-api [api]`
- `/security-controls [system]`
- `/compliance-map [standard]`

### compliance-check.md

**Capacidades:**
- Mapeo a estándares (NIST, ISO, OWASP)
- Compliance regulatorio (GDPR, HIPAA, PCI)
- Gap analysis
- Preparación de auditorías

**Comandos:**
- `/compliance-check [standard]`
- `/gap-analysis [standard]`
- `/control-map [control]`
- `/audit-prep [standard]`

---

## 🟣 Integración con Purple Team

### Colaboración con Red Team 🔴

| Yellow Team Provee | Red Team Usa Para |
|--------------------|-------------------|
| Threat models | Planificación de ataques |
| Attack trees | Identificación de paths |
| Vectores de ataque | Scope de pentesting |
| Arquitectura | Reconocimiento |

### Colaboración con Blue Team 🔵

| Yellow Team Provee | Blue Team Usa Para |
|--------------------|-------------------|
| Requisitos de logging | Configuración SIEM |
| Controles requeridos | Implementación |
| Threat models | Reglas de detección |
| Compliance mapping | Auditorías |

### Flujo Purple Team

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PURPLE TEAM WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🟡 YELLOW TEAM                                                            │
│   ┌─────────────────┐                                                       │
│   │ 1. Threat Model │──────────────────────────────────────┐               │
│   │ 2. Attack Trees │                                      │               │
│   │ 3. Requirements │                                      ▼               │
│   └─────────────────┘                              ┌───────────────┐       │
│                                                    │ 🔴 RED TEAM   │       │
│                                                    │ - Test attacks│       │
│                                                    │ - Validate    │       │
│                                                    │ - Report      │       │
│                                                    └───────┬───────┘       │
│                                                            │               │
│   ┌─────────────────┐                                      │               │
│   │ 🟡 UPDATE       │◄─────────────────────────────────────┤               │
│   │ - Threat model  │                                      │               │
│   │ - Requirements  │                                      ▼               │
│   │ - Architecture  │                              ┌───────────────┐       │
│   └─────────────────┘                              │ 🔵 BLUE TEAM  │       │
│                                                    │ - Implement   │       │
│                                                    │ - Detect      │       │
│                                                    │ - Respond     │       │
│                                                    └───────────────┘       │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    CONTINUOUS IMPROVEMENT LOOP                      │  │
│   │  Yellow designs → Red tests → Blue defends → Yellow updates → ...  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📖 Guía de Uso

### Quick Start

```bash
# 1. Entrar al workspace
cd "YellowTeam - Windsurf"

# 2. Ejecutar instalador
chmod +x install.sh && ./install.sh

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Abrir en Windsurf
windsurf YellowTeam.code-workspace
```

### Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `/threat-model` | Crear threat model |
| `/review-arch` | Revisar arquitectura |
| `/zero-trust` | Validar Zero Trust |
| `/attack-tree` | Generar attack tree |
| `/security-reqs` | Generar requisitos |

### Flujo de Trabajo Típico

```
1. Recibir arquitectura/diseño
         │
         ▼
2. /threat-model
   - Identificar componentes
   - Crear DFD
   - Aplicar STRIDE
   - Documentar amenazas
         │
         ▼
3. /review-arch
   - Evaluar controles
   - Identificar gaps
   - Documentar findings
         │
         ▼
4. /zero-trust
   - Validar principios
   - Evaluar madurez
   - Recomendar mejoras
         │
         ▼
5. /security-reqs
   - Generar requisitos
   - Mapear a estándares
   - Crear traceability
         │
         ▼
6. Entregar documentación
   - Threat model
   - Security review
   - Requirements spec
   - Recommendations
```

---

## 🔧 Mantenimiento

### Actualización de Dependencias

```bash
# Activar venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Actualizar dependencias
pip install --upgrade -r requirements.txt
```

### Actualización de Templates

Los templates se encuentran en:
- `templates/threat-models/`
- `templates/architectures/`
- `templates/requirements/`

### Backup de Trabajo

```bash
# Crear backup
tar -czvf yellow-team-backup-$(date +%Y%m%d).tar.gz \
    threat-models/ \
    reviews/ \
    requirements/ \
    reports/
```

### Limpieza

```bash
# Limpiar archivos temporales
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete
find . -name ".DS_Store" -delete
```

---

## 📊 Métricas y KPIs

### Métricas de Threat Modeling

| Métrica | Descripción | Target |
|---------|-------------|--------|
| Cobertura STRIDE | % de componentes analizados | 100% |
| Threats/Component | Amenazas por componente | 3-5 |
| Mitigations/Threat | Mitigaciones por amenaza | 1-3 |
| Critical Threats | Amenazas críticas identificadas | Minimizar |

### Métricas de Architecture Review

| Métrica | Descripción | Target |
|---------|-------------|--------|
| Security Score | Puntuación de seguridad | >80% |
| Critical Findings | Hallazgos críticos | 0 |
| High Findings | Hallazgos altos | <3 |
| Compliance Coverage | Cobertura de compliance | >90% |

### Métricas de Zero Trust

| Métrica | Descripción | Target |
|---------|-------------|--------|
| Maturity Score | Puntuación de madurez | >70% |
| Identity Controls | Controles de identidad | 100% |
| Network Segmentation | Segmentación de red | Implementado |
| Encryption Coverage | Cobertura de cifrado | 100% |

---

## 🔗 Referencias

### Frameworks y Estándares
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)
- [OWASP](https://owasp.org/)
- [SABSA](https://sabsa.org/)
- [TOGAF](https://www.opengroup.org/togaf)

### Threat Modeling
- [Microsoft Threat Modeling](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [STRIDE](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [PASTA](https://owasp.org/www-pdf-archive/AppSecEU2012_PASTA.pdf)

### Zero Trust
- [NIST Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)
- [Google BeyondCorp](https://cloud.google.com/beyondcorp)
- [Microsoft Zero Trust](https://www.microsoft.com/en-us/security/business/zero-trust)

---

<div align="center">

## 🟡 Yellow Team

**"Security by Design, Not by Accident"**

---

*Documento generado automáticamente*
*Fecha: 2024*

</div>
]]>
