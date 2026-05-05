# 🟣 MEMORIA DE CONSTRUCCIÓN - Purple Team Windsurf

## 📋 Información del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | Purple Team Windsurf |
| **Versión** | 1.0.0 |
| **Fecha de Creación** | 2024 |
| **Plataforma** | Kali Linux + Windsurf AI |
| **Propósito** | Validación continua de controles de seguridad |

---

## 🎯 Objetivo del Workspace

Este workspace está diseñado para ejecutar ejercicios de **Purple Team**, combinando las capacidades ofensivas del Red Team con las defensivas del Blue Team para:

1. **Simular ataques** basados en MITRE ATT&CK
2. **Validar detecciones** en múltiples fuentes
3. **Identificar brechas** de seguridad
4. **Generar reportes** ejecutivos y técnicos
5. **Mejorar continuamente** las defensas

---

## 🏗️ Arquitectura del Workspace

```
PurpleTeam-Windsurf/
│
├── 📄 README.md                    # Documentación principal
├── 📄 memoria.md                   # Este archivo
├── 🔧 install.sh                   # Instalador completo
├── ⚙️ .windsurfrules               # Reglas para Windsurf AI
│
├── 🔴 attacks/                     # Simulaciones ejecutadas
│   ├── T1003.001/                  # Por técnica ATT&CK
│   ├── T1059.001/
│   └── ...
│
├── 🔵 detections/                  # Validaciones de detección
│   ├── T1003.001/
│   ├── T1059.001/
│   └── ...
│
├── 🟣 gaps/                        # Brechas identificadas
│   ├── analysis/                   # Análisis de gaps
│   └── recommendations/            # Recomendaciones
│
├── 🗺️ mitre/                       # Mapeo ATT&CK
│   ├── coverage/                   # Cobertura actual
│   ├── navigator/                  # Archivos Navigator
│   └── techniques/                 # Técnicas documentadas
│
├── 📚 playbooks/                   # Playbooks de ejercicios
│   ├── red/                        # Playbooks ofensivos
│   ├── blue/                       # Playbooks defensivos
│   └── purple/                     # Ejercicios integrados
│
├── 📊 reports/                     # Reportes generados
│   ├── exercises/                  # Reportes de ejercicios
│   ├── gaps/                       # Reportes de brechas
│   └── metrics/                    # Métricas y KPIs
│
├── 📜 rules/                       # Reglas de detección
│   ├── sigma/                      # Sigma rules
│   └── yara/                       # YARA rules
│
├── 🎭 simulations/                 # Escenarios de simulación
│   ├── apt/                        # Simulaciones APT
│   ├── ransomware/                 # Simulaciones ransomware
│   └── insider/                    # Amenazas internas
│
├── 🔧 tools/                       # Scripts y herramientas
│   ├── custom-scripts/
│   │   ├── attack_simulate.py      # Simular técnicas
│   │   ├── detection_validate.sh   # Validar detecciones
│   │   ├── gap_analyzer.py         # Analizar brechas
│   │   ├── mitre_mapper.py         # Mapear ATT&CK
│   │   └── purple_report.py        # Generar reportes
│   └── external/                   # Herramientas externas
│
├── 📂 skills/                      # Skills de Windsurf
│
├── 📂 .windsurf/                   # Configuración Windsurf
│   └── workflows/
│       ├── simulate.md
│       ├── validate.md
│       ├── gap-analysis.md
│       └── purple-exercise.md
│
├── 📂 logs/                        # Logs de ejercicios
├── 📂 evidence/                    # Evidencia recolectada
└── 📂 templates/                   # Plantillas
```

---

## 🛠️ Componentes Desarrollados

### 1. Scripts Personalizados

#### `attack_simulate.py`
- **Propósito**: Simular técnicas MITRE ATT&CK
- **Características**:
  - Base de datos de técnicas ATT&CK integrada
  - Soporte para Atomic Red Team, Caldera, scripts custom
  - Generación automática de evidencia
  - Documentación en formato YAML
- **Uso**: `python attack_simulate.py --technique T1003.001`

#### `detection_validate.sh`
- **Propósito**: Validar detecciones en múltiples fuentes
- **Características**:
  - Verificación de reglas Sigma
  - Verificación de reglas YARA
  - Consulta de eventos Sysmon
  - Consulta de eventos Windows Security
  - Cálculo de cobertura
- **Uso**: `./detection_validate.sh T1003.001`

#### `gap_analyzer.py`
- **Propósito**: Analizar brechas de detección
- **Características**:
  - Identificación de técnicas sin cobertura
  - Clasificación por severidad
  - Generación de recomendaciones
  - Sugerencias de reglas Sigma
- **Uso**: `python gap_analyzer.py --full-analysis`

#### `mitre_mapper.py`
- **Propósito**: Mapeo y visualización ATT&CK
- **Características**:
  - Base de datos de tácticas y técnicas
  - Mapa de cobertura
  - Exportación para ATT&CK Navigator
- **Uso**: `python mitre_mapper.py --coverage-map`

#### `purple_report.py`
- **Propósito**: Generación de reportes
- **Características**:
  - Reporte de ejercicio
  - Reporte de brechas
  - Reporte de métricas
  - Resumen ejecutivo
- **Uso**: `python purple_report.py --full-report`

### 2. Workflows de Windsurf

| Workflow | Comando | Descripción |
|----------|---------|-------------|
| simulate | `/simulate T1003.001` | Simular técnica ATT&CK |
| validate | `/validate T1003.001` | Validar detección |
| gap-analysis | `/gap-analysis` | Analizar brechas |
| purple-exercise | `/purple-exercise` | Ejercicio completo |

### 3. Reglas de Windsurf (.windsurfrules)

Las reglas configuran a Windsurf AI para:
- Actuar como experto en Purple Team
- Seguir metodología de ciclo Purple Team
- Documentar en formato YAML
- Generar recomendaciones específicas
- Mapear a MITRE ATT&CK

---

## 🔧 Herramientas Integradas

### Red Team (Ofensivas)

| Herramienta | Propósito | Instalación |
|-------------|-----------|-------------|
| Atomic Red Team | Tests atómicos ATT&CK | install.sh |
| MITRE Caldera | Adversary emulation | install.sh |
| Infection Monkey | Breach simulation | Docker |
| Stratus Red Team | Cloud attacks | Go install |
| Metasploit | Penetration testing | Kali nativo |
| CrackMapExec | Post-exploitation | Kali nativo |
| BloodHound | AD attack paths | Kali nativo |
| Impacket | Network protocols | pip |

### Blue Team (Defensivas)

| Herramienta | Propósito | Instalación |
|-------------|-----------|-------------|
| Sigma | Detection rules | Git clone |
| YARA | Malware detection | apt |
| Velociraptor | Endpoint visibility | Binary |
| Wazuh | SIEM/XDR | Docker |
| Zeek | Network monitoring | apt |
| Volatility | Memory forensics | apt |
| Suricata | IDS/IPS | apt |

### Purple Team

| Herramienta | Propósito | Instalación |
|-------------|-----------|-------------|
| DetectionLab | Lab environment | Git clone |
| DeTTECT | ATT&CK scoring | Git clone |
| ATT&CK Navigator | Visualization | Docker |
| Vectr | Tracking | Docker |

---

## 📊 Métricas y KPIs

### Métricas Principales

| Métrica | Descripción | Objetivo |
|---------|-------------|----------|
| **Cobertura ATT&CK** | % de técnicas con detección | ≥70% |
| **MTTD** | Mean Time to Detect | <15 min |
| **MTTR** | Mean Time to Respond | <1 hora |
| **Tasa de Detección** | Técnicas detectadas/probadas | ≥80% |
| **Falsos Positivos** | Alertas incorrectas | <5% |

### Clasificación de Brechas

| Severidad | Descripción | SLA |
|-----------|-------------|-----|
| 🔴 Crítica | Técnica de alto impacto sin detección | 24 horas |
| 🟠 Alta | Técnica común sin cobertura | 1 semana |
| 🟡 Media | Cobertura parcial | 2 semanas |
| 🔵 Baja | Optimizaciones menores | 1 mes |

---

## 🔄 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CICLO PURPLE TEAM                               │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  1. PLANIFICAR                                                      │
│     • Seleccionar técnicas ATT&CK                                   │
│     • Definir alcance y objetivos                                   │
│     • Preparar ambiente                                             │
│     Comando: /purple-exercise --scenario <scenario>                 │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. SIMULAR (Red Team)                                              │
│     • Ejecutar técnicas ATT&CK                                      │
│     • Documentar comandos y artefactos                              │
│     • Capturar evidencia                                            │
│     Comando: /simulate T1003.001                                    │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. DETECTAR (Blue Team)                                            │
│     • Verificar alertas en SIEM/EDR                                 │
│     • Validar reglas Sigma/YARA                                     │
│     • Medir tiempo de detección                                     │
│     Comando: /validate T1003.001                                    │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. ANALIZAR (Purple Team)                                          │
│     • Identificar brechas                                           │
│     • Clasificar por severidad                                      │
│     • Generar recomendaciones                                       │
│     Comando: /gap-analysis                                          │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. MEJORAR                                                         │
│     • Implementar reglas de detección                               │
│     • Actualizar playbooks                                          │
│     • Configurar alertas                                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  6. VALIDAR                                                         │
│     • Re-ejecutar técnicas                                          │
│     • Confirmar detección                                           │
│     • Documentar mejora                                             │
│     Comando: /simulate T1003.001 (re-test)                          │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                          🔁 REPETIR
```

---

## 📁 Formato de Datos

### Ataque Simulado (YAML)

```yaml
technique_id: T1003.001
technique_name: OS Credential Dumping: LSASS Memory
tactic: Credential Access
tool: atomic-red-team
command: Invoke-AtomicTest T1003.001
timestamp_start: 2024-01-15T10:30:00
timestamp_end: 2024-01-15T10:30:05
status: success
output: |
  [SIMULACIÓN] Técnica ejecutada exitosamente
artifacts:
  - evidence/T1003.001/20240115_103000/lsass.dmp
evidence_hash: sha256:abc123...
```

### Detección Validada (YAML)

```yaml
technique_id: T1003.001
validation_timestamp: 2024-01-15T10:35:00
coverage: 85
detection_sources:
  - source: sysmon
    detected: true
    event_id: 10
    time_to_detect: 120  # segundos
  - source: edr
    detected: true
    alert_name: LSASS Access
    time_to_detect: 30
  - source: sigma
    detected: true
    rule: proc_access_win_lsass_memdump.yml
false_positives: 0
```

### Brecha Identificada (YAML)

```yaml
technique_id: T1055.001
technique_name: Process Injection: DLL Injection
tactic: Defense Evasion
gap_type: no_detection
severity: critical
description: No existe detección para DLL Injection
current_coverage: 0
expected_coverage: 80
detection_sources_missing:
  - sysmon
  - edr
  - sigma
recommendations:
  - Implementar regla Sigma para CreateRemoteThread
  - Habilitar Sysmon Event 8
  - Configurar alerta EDR
sigma_rule_suggestion: |
  title: CreateRemoteThread API Call
  ...
priority_score: 95
remediation_status: pending
assigned_to: blue_team
due_date: 2024-01-22
```

---

## 🚀 Instalación y Configuración

### Requisitos

- Kali Linux 2023.x o superior
- Python 3.10+
- Docker y Docker Compose
- Git
- 8GB RAM mínimo
- 50GB espacio en disco

### Instalación

```bash
# 1. Clonar/Crear workspace
cd ~/Documents/PurpleTeam\ -\ Windsurf

# 2. Ejecutar instalador
chmod +x install.sh
sudo ./install.sh

# 3. Activar entorno
source venv/bin/activate

# 4. Verificar instalación
python tools/custom-scripts/attack_simulate.py --list-techniques
```

### Servicios Docker

```bash
# Iniciar servicios
cd tools && docker-compose up -d

# Servicios disponibles:
# - Elasticsearch: http://localhost:9200
# - Kibana: http://localhost:5601
# - Caldera: http://localhost:8888
# - Portainer: http://localhost:9000
```

---

## 🔐 Consideraciones de Seguridad

### Ambiente Controlado

- ✅ Solo ejecutar en sistemas autorizados
- ✅ Documentar todas las acciones
- ✅ Tener plan de rollback
- ✅ Notificar al equipo antes de ejercicios
- ❌ No afectar sistemas de producción

### Manejo de Evidencia

- Preservar integridad de logs
- Hashear artefactos recolectados
- Almacenar en ubicación segura
- Mantener cadena de custodia
- Retener según política

### Credenciales

- No hardcodear credenciales
- Usar variables de entorno
- Rotar credenciales regularmente
- Documentar accesos requeridos

---

## 📈 Roadmap

### Versión 1.1
- [ ] Integración con Splunk
- [ ] Integración con Elastic SIEM
- [ ] Dashboard web interactivo
- [ ] API REST para automatización

### Versión 1.2
- [ ] Soporte para cloud (AWS, Azure, GCP)
- [ ] Integración con SOAR
- [ ] Machine learning para detección
- [ ] Reportes automatizados por email

### Versión 2.0
- [ ] Multi-tenancy
- [ ] Colaboración en tiempo real
- [ ] Integración con ticketing
- [ ] Métricas históricas y tendencias

---

## 📚 Referencias

### MITRE ATT&CK
- https://attack.mitre.org/
- https://attack.mitre.org/techniques/enterprise/

### Herramientas
- Atomic Red Team: https://github.com/redcanaryco/atomic-red-team
- MITRE Caldera: https://github.com/mitre/caldera
- Sigma: https://github.com/SigmaHQ/sigma
- YARA: https://github.com/VirusTotal/yara

### Documentación
- Purple Team Exercise Framework: https://github.com/scythe-io/purple-team-exercise-framework
- DeTTECT: https://github.com/rabobank-cdc/DeTTECT

---

## 👥 Contribución

Para contribuir a este proyecto:

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-feature`)
3. Commit cambios (`git commit -m 'Add nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abrir Pull Request

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles.

---

<div align="center">

**🟣 Purple Team Windsurf**

*Validación Continua de Seguridad*

Hecho con 💜 para la comunidad de seguridad

</div>
