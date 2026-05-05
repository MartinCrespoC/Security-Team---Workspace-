# 🟡 YELLOW TEAM - Security Architecture & Threat Modeling

![Team Yellow](https://img.shields.io/badge/Team-Yellow-FFD700?style=for-the-badge&labelColor=000000)
![Security Architecture](https://img.shields.io/badge/Focus-Security%20Architecture-FFD700?style=for-the-badge&labelColor=000000)
![Windsurf AI](https://img.shields.io/badge/Powered%20by-Windsurf%20AI-00D4FF?style=for-the-badge&labelColor=000000)

> **"Security by Design, Not by Accident"**

---

## 🎯 ¿Qué es Yellow Team?

El **Yellow Team** es el equipo de **Arquitectura de Seguridad** responsable de diseñar sistemas seguros desde el inicio, realizar threat modeling y validar arquitecturas contra principios de Zero Trust.

| Función | Descripción |
|---------|-------------|
| 🏗️ **Diseño Seguro** | Arquitecturas resilientes desde el inicio |
| 🔍 **Threat Modeling** | STRIDE, PASTA, Attack Trees |
| 🛡️ **Zero Trust** | Validación de principios ZT |
| 📋 **Requisitos** | Especificaciones de seguridad |
| 📊 **Reviews** | Revisiones de arquitectura |

---

## 🚀 Quick Start

```bash
# 1. Clonar repositorio
git clone https://github.com/MartinCrespoC/YellowTeam---Windsurf.git
cd YellowTeam---Windsurf

# 2. Instalar dependencias
chmod +x install.sh && ./install.sh

# 3. Activar entorno
source venv/bin/activate

# 4. Abrir en Windsurf
windsurf YellowTeam.code-workspace
```

### Comandos Rápidos

| Comando | Descripción |
|---------|-------------|
| `/threat-model` | Crear threat model con STRIDE |
| `/review-arch` | Revisar arquitectura |
| `/zero-trust` | Validar Zero Trust |

---

## 📚 Metodologías

### STRIDE

Metodología de threat modeling por categorías:

| Categoría | Amenaza | Propiedad | Mitigación |
|-----------|---------|-----------|------------|
| **S**poofing | Suplantación de identidad | Autenticación | MFA, certificados |
| **T**ampering | Modificación de datos | Integridad | Firmas, validación |
| **R**epudiation | Negar acciones | No repudio | Logs, auditoría |
| **I**nfo Disclosure | Exposición de datos | Confidencialidad | Cifrado, ACL |
| **D**enial of Service | Interrupción | Disponibilidad | Rate limiting, HA |
| **E**levation | Escalada de privilegios | Autorización | RBAC, least privilege |

### PASTA

**Process for Attack Simulation and Threat Analysis** - 7 etapas:

1. **Define Objectives** - Objetivos de negocio y seguridad
2. **Define Technical Scope** - Límites y dependencias
3. **Application Decomposition** - DFDs y assets
4. **Threat Analysis** - Actores y vectores
5. **Vulnerability Analysis** - Debilidades
6. **Attack Modeling** - Árboles de ataque
7. **Risk & Impact** - Evaluación y contramedidas

### Zero Trust

> *"Never Trust, Always Verify"*

| Principio | Descripción |
|-----------|-------------|
| **Verify Explicitly** | Autenticar siempre con todos los datos disponibles |
| **Least Privilege** | Acceso mínimo necesario (JIT/JEA) |
| **Assume Breach** | Minimizar radio de explosión, segmentar |

---

## 🔧 Herramientas

### Scripts Incluidos

| Script | Descripción |
|--------|-------------|
| `threat_model.py` | Generador de threat models |
| `architecture_review.py` | Revisor de arquitectura |
| `zero_trust_check.sh` | Validador Zero Trust |
| `attack_tree.py` | Generador de attack trees |
| `security_requirements.py` | Generador de requisitos |

### Uso

```bash
# Threat Model interactivo
python tools/custom-scripts/threat_model.py -i

# Revisión de arquitectura
python tools/custom-scripts/architecture_review.py -i

# Validación Zero Trust
bash tools/custom-scripts/zero_trust_check.sh

# Attack Trees
python tools/custom-scripts/attack_tree.py -i

# Requisitos de seguridad
python tools/custom-scripts/security_requirements.py -i
```

---

## 📁 Estructura

```
YellowTeam-Windsurf/
├── README.md
├── memoria.md              # Documentación detallada
├── install.sh              # Instalador
├── .windsurfrules          # Reglas AI
│
├── threat-models/          # Modelos de amenazas
├── architectures/          # Diagramas
├── requirements/           # Requisitos de seguridad
├── reviews/                # Revisiones
├── patterns/               # Patrones seguros
├── frameworks/             # SABSA, TOGAF, NIST
│
├── tools/custom-scripts/   # Scripts Python/Bash
│
└── .windsurf/
    ├── workflows/          # /threat-model, /review-arch, /zero-trust
    └── skills/             # AI skills
```

---

## 🔄 Workflows

### /threat-model

1. Recopilar información del sistema
2. Crear Data Flow Diagram (DFD)
3. Aplicar análisis STRIDE
4. Documentar amenazas
5. Proponer mitigaciones
6. Generar reporte

### /review-arch

Checklist de seguridad:

- ✅ Authentication (MFA, sessions)
- ✅ Authorization (RBAC, least privilege)
- ✅ Data Protection (encryption, keys)
- ✅ Network (segmentation, WAF)
- ✅ Logging (SIEM, alerts)
- ✅ Application (input validation, headers)

### /zero-trust

Validación de pilares:

- 🔐 **Identity** - MFA, continuous validation
- 💻 **Devices** - Health, compliance
- 🌐 **Network** - Micro-segmentation, encryption
- 📱 **Applications** - AuthN/AuthZ per request
- 📊 **Data** - Classification, DLP
- 👁️ **Visibility** - Monitoring, analytics

---

## 🤝 Purple Team Integration

| Team | Aporta | Recibe |
|------|--------|--------|
| 🟡 Yellow | Threat models, requirements | Findings de Red/Blue |
| 🔴 Red | Validación de amenazas | Scope de Yellow |
| 🔵 Blue | Detecciones implementadas | Controles de Yellow |

---

## 🛡️ Frameworks Soportados

| Framework | Uso |
|-----------|-----|
| **NIST CSF** | Identify, Protect, Detect, Respond, Recover |
| **ISO 27001** | Sistema de gestión de seguridad |
| **OWASP** | Seguridad de aplicaciones |
| **SABSA** | Arquitectura de seguridad empresarial |
| **TOGAF** | Arquitectura empresarial + seguridad |
| **CIS Controls** | Controles de seguridad prioritizados |

---

## 📖 Documentación

- [memoria.md](memoria.md) - Documentación completa de construcción
- [install.sh](install.sh) - Script de instalación
- [.windsurfrules](.windsurfrules) - Reglas para Windsurf AI

---

## 🟡 Yellow Team

*Diseñando el futuro seguro*

> **"Security is not a product, but a process"** - Bruce Schneier

---

Made with 💛 for Security Architects
