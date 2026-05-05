# 🟣 PURPLE TEAM SKILLS

## Descripción
Skills para operaciones colaborativas de Purple Team, combinando Red y Blue Team.

---

## Metodología Purple Team

### Ciclo de Validación

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   1. PLANIFICAR    2. SIMULAR    3. DETECTAR    4. ANALIZAR        │
│        │               │              │              │              │
│        ▼               ▼              ▼              ▼              │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│   │ Técnica │───►│ Ataque  │───►│ Alerta  │───►│ Brecha  │         │
│   │ ATT&CK  │    │ Simulado│    │ Generada│    │ Análisis│         │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│        │               │              │              │              │
│        └───────────────┴──────────────┴──────────────┘              │
│                              │                                      │
│                              ▼                                      │
│                    5. MEJORAR ──► 6. VALIDAR                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Framework de Ejercicios

```yaml
exercise:
  name: "Purple Team Exercise - Q1 2024"
  objective: "Validar controles de Credential Access"
  scope:
    techniques:
      - T1003.001  # LSASS Memory
      - T1003.002  # SAM Database
      - T1110.001  # Password Guessing
    systems:
      - Windows Server 2019
      - Windows 10 Workstations
    duration: "4 hours"
  
  team:
    red_team:
      - Ejecutar simulaciones
      - Documentar comandos
      - Capturar evidencia
    blue_team:
      - Monitorear alertas
      - Validar detecciones
      - Medir tiempos
    purple_lead:
      - Coordinar ejercicio
      - Analizar brechas
      - Generar reporte
  
  success_criteria:
    - coverage: ">= 80%"
    - mttd: "<= 15 min"
    - false_positives: "<= 5%"
```

---

## Escenarios de Ejercicio

### Escenario 1: Credential Theft

```yaml
name: Credential Theft Scenario
description: Simular robo de credenciales end-to-end
duration: 2 hours

phases:
  - name: Initial Access
    techniques:
      - T1566.001  # Spearphishing Attachment
    actions:
      - Enviar email con documento malicioso
      - Ejecutar macro
    expected_detections:
      - Email gateway alert
      - EDR macro execution alert

  - name: Execution
    techniques:
      - T1059.001  # PowerShell
    actions:
      - Ejecutar PowerShell encoded
      - Download cradle
    expected_detections:
      - PowerShell Script Block Logging
      - Sysmon Event 1

  - name: Credential Access
    techniques:
      - T1003.001  # LSASS Memory
    actions:
      - Dump LSASS con Mimikatz
      - Extraer hashes
    expected_detections:
      - Sysmon Event 10
      - EDR LSASS access alert

  - name: Lateral Movement
    techniques:
      - T1021.002  # SMB Admin Shares
    actions:
      - Pass-the-hash
      - Acceso a C$
    expected_detections:
      - Event 4624 Type 3
      - Event 5140 Admin Share
```

### Escenario 2: Ransomware Simulation

```yaml
name: Ransomware Simulation
description: Simular ataque de ransomware
duration: 3 hours

phases:
  - name: Initial Compromise
    techniques:
      - T1566.002  # Spearphishing Link
    
  - name: Reconnaissance
    techniques:
      - T1082  # System Information Discovery
      - T1083  # File and Directory Discovery
    
  - name: Lateral Movement
    techniques:
      - T1021.001  # RDP
      - T1021.002  # SMB
    
  - name: Collection
    techniques:
      - T1005  # Data from Local System
    
  - name: Impact
    techniques:
      - T1486  # Data Encrypted for Impact
      - T1490  # Inhibit System Recovery
    actions:
      - Simular encriptación (sin daño real)
      - Eliminar shadow copies (simulado)
    expected_detections:
      - Ransomware behavior alert
      - Volume shadow copy deletion
      - Mass file modification
```

### Escenario 3: APT Simulation

```yaml
name: APT Simulation
description: Simular campaña APT completa
duration: 8 hours

kill_chain:
  - reconnaissance:
      techniques: [T1595, T1592]
      duration: 1h
      
  - weaponization:
      techniques: [T1587.001]
      duration: 30m
      
  - delivery:
      techniques: [T1566.001]
      duration: 30m
      
  - exploitation:
      techniques: [T1203]
      duration: 30m
      
  - installation:
      techniques: [T1547.001, T1053.005]
      duration: 1h
      
  - command_and_control:
      techniques: [T1071.001, T1573.001]
      duration: 1h
      
  - actions_on_objectives:
      techniques: [T1003.001, T1005, T1048.003]
      duration: 3h
```

---

## Matriz de Detección

### Template de Cobertura

```markdown
| Técnica | Nombre | Sysmon | EDR | SIEM | Sigma | Total |
|---------|--------|--------|-----|------|-------|-------|
| T1003.001 | LSASS Memory | ✅ | ✅ | ✅ | ✅ | 100% |
| T1003.002 | SAM Database | ✅ | ⚠️ | ✅ | ✅ | 75% |
| T1059.001 | PowerShell | ✅ | ✅ | ✅ | ✅ | 100% |
| T1547.001 | Registry Run Keys | ✅ | ✅ | ⚠️ | ✅ | 75% |
| T1055.001 | DLL Injection | ⚠️ | ✅ | ❌ | ⚠️ | 50% |
| T1070.001 | Clear Event Logs | ✅ | ✅ | ✅ | ✅ | 100% |

Leyenda:
✅ = Detectado (>80%)
⚠️ = Parcial (40-80%)
❌ = No detectado (<40%)
```

### Gap Analysis Template

```yaml
gap_analysis:
  technique: T1055.001
  technique_name: DLL Injection
  
  current_state:
    coverage: 50%
    detection_sources:
      - sysmon: partial
      - edr: detected
      - siem: not_detected
      - sigma: partial
    
  root_cause:
    - Sysmon Event 8 no habilitado
    - Regla Sigma no implementada
    - SIEM no recibe eventos de CreateRemoteThread
    
  recommendations:
    - priority: high
      action: "Habilitar Sysmon Event 8 (CreateRemoteThread)"
      owner: "Blue Team"
      due_date: "+3 days"
      
    - priority: high
      action: "Implementar regla Sigma para process injection"
      owner: "Detection Engineering"
      due_date: "+5 days"
      
    - priority: medium
      action: "Configurar forwarding de eventos a SIEM"
      owner: "SOC"
      due_date: "+7 days"
      
  validation:
    - Re-ejecutar T1055.001 después de implementar
    - Verificar cobertura >= 80%
    - Documentar resultados
```

---

## Métricas y KPIs

### Dashboard de Métricas

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PURPLE TEAM METRICS DASHBOARD                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  COBERTURA ATT&CK          MTTD (Mean Time to Detect)              │
│  ┌────────────────┐        ┌────────────────┐                      │
│  │ ████████░░ 78% │        │     2.5 min    │                      │
│  │ Target: 80%    │        │ Target: <15min │                      │
│  └────────────────┘        └────────────────┘                      │
│                                                                     │
│  TÉCNICAS PROBADAS         BRECHAS CRÍTICAS                        │
│  ┌────────────────┐        ┌────────────────┐                      │
│  │      45/60     │        │       2        │                      │
│  │     (75%)      │        │  Target: 0     │                      │
│  └────────────────┘        └────────────────┘                      │
│                                                                     │
│  TENDENCIA DE COBERTURA                                            │
│  100% │                                    ╭──                     │
│   80% │                           ╭───────╯                        │
│   60% │              ╭───────────╯                                 │
│   40% │     ╭───────╯                                              │
│   20% │────╯                                                       │
│    0% └────────────────────────────────────────────                │
│        Ene   Feb   Mar   Abr   May   Jun                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Cálculo de Métricas

```python
# Cobertura ATT&CK
coverage = (techniques_detected / techniques_tested) * 100

# MTTD (Mean Time to Detect)
mttd = sum(detection_times) / len(detection_times)

# MTTR (Mean Time to Respond)
mttr = sum(response_times) / len(response_times)

# Tasa de Falsos Positivos
fp_rate = (false_positives / total_alerts) * 100

# Score de Madurez
maturity_score = (
    (coverage * 0.3) +
    (detection_rate * 0.3) +
    (response_rate * 0.2) +
    (documentation_score * 0.2)
)
```

---

## Reportes

### Reporte Ejecutivo Template

```markdown
# Purple Team Exercise Report
## Executive Summary

**Fecha:** YYYY-MM-DD
**Duración:** X horas
**Técnicas Probadas:** N

### Estado General: 🟡 BUENO

### Métricas Clave
| Métrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| Cobertura | 78% | 80% | ⚠️ |
| MTTD | 2.5 min | <15 min | ✅ |
| Brechas Críticas | 2 | 0 | ❌ |

### Hallazgos Principales
1. **Crítico**: T1055.001 (DLL Injection) sin detección
2. **Alto**: T1003.002 (SAM) detección parcial
3. **Medio**: Latencia en alertas de PowerShell

### Recomendaciones
1. Implementar detección de process injection
2. Mejorar reglas de acceso a SAM
3. Optimizar pipeline de alertas

### Próximos Pasos
- [ ] Implementar correcciones (1 semana)
- [ ] Re-validar técnicas críticas
- [ ] Programar siguiente ejercicio
```

### Reporte Técnico Template

```markdown
# Purple Team Technical Report

## Técnicas Ejecutadas

### T1003.001 - LSASS Memory
**Estado:** ✅ Detectado

**Simulación:**
- Herramienta: Atomic Red Team
- Comando: `Invoke-AtomicTest T1003.001`
- Timestamp: 2024-01-15 10:30:00

**Detección:**
| Fuente | Detectado | Tiempo | Alerta |
|--------|-----------|--------|--------|
| Sysmon | ✅ | 30s | Event 10 |
| EDR | ✅ | 15s | LSASS Access |
| SIEM | ✅ | 2min | Correlation Rule |

**Evidencia:**
- attacks/T1003.001/20240115_103000.yaml
- evidence/T1003.001/sysmon_event.xml

---

### T1055.001 - DLL Injection
**Estado:** ❌ No Detectado

**Simulación:**
- Herramienta: Custom Script
- Comando: `inject.exe -p <pid> -d test.dll`
- Timestamp: 2024-01-15 11:00:00

**Detección:**
| Fuente | Detectado | Tiempo | Alerta |
|--------|-----------|--------|--------|
| Sysmon | ❌ | N/A | - |
| EDR | ⚠️ | 5min | Low confidence |
| SIEM | ❌ | N/A | - |

**Gap Analysis:**
- Sysmon Event 8 no habilitado
- Regla Sigma no existe
- EDR requiere tuning

**Recomendación:**
```yaml
title: CreateRemoteThread Detection
logsource:
    category: create_remote_thread
    product: windows
detection:
    selection:
        EventType: CreateRemoteThread
    condition: selection
```
```

---

## Herramientas Purple Team

| Herramienta | Propósito | Uso |
|-------------|-----------|-----|
| Atomic Red Team | Simulación | Tests atómicos |
| MITRE Caldera | Adversary emulation | Campañas |
| DeTTECT | ATT&CK scoring | Gap analysis |
| ATT&CK Navigator | Visualización | Mapas |
| Vectr | Tracking | Documentación |
| Splunk Attack Range | Lab | Ambiente integrado |

---

## Comandos Rápidos

```bash
# Simular técnica
python attack_simulate.py --technique T1003.001

# Validar detección
./detection_validate.sh T1003.001

# Analizar brechas
python gap_analyzer.py --full-analysis

# Generar reporte
python purple_report.py --full-report

# Exportar Navigator
python mitre_mapper.py --export-navigator
```
