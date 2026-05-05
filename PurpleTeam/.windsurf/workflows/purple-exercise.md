---
description: Ejecutar ejercicio completo de Purple Team con múltiples técnicas
---

# /purple-exercise - Ejercicio Purple Team Completo

Este workflow ejecuta un ciclo completo de Purple Team: simulación, detección, análisis y reporte.

## Uso

```
/purple-exercise
/purple-exercise --scenario credential-theft
/purple-exercise --techniques T1003.001,T1059.001,T1547.001
/purple-exercise --quick
```

## Pasos del Workflow

### 1. Planificación
Definir alcance del ejercicio:
- Técnicas a probar
- Sistemas objetivo
- Duración estimada
- Equipo participante

### 2. Preparación del Ambiente
Verificar que todo está listo:

// turbo
```bash
python tools/custom-scripts/attack_simulate.py --list-techniques
```

### 3. Notificación
Informar al equipo:
- Blue Team: Monitoreo activo
- SOC: Ejercicio en progreso
- Stakeholders: Ventana de pruebas

### 4. Ejecución de Simulaciones
Ejecutar técnicas en secuencia:

```bash
# Técnica 1: Credential Access
python tools/custom-scripts/attack_simulate.py --technique T1003.001

# Técnica 2: Execution
python tools/custom-scripts/attack_simulate.py --technique T1059.001

# Técnica 3: Persistence
python tools/custom-scripts/attack_simulate.py --technique T1547.001
```

### 5. Validación de Detecciones
Verificar cada técnica:

```bash
./tools/custom-scripts/detection_validate.sh T1003.001
./tools/custom-scripts/detection_validate.sh T1059.001
./tools/custom-scripts/detection_validate.sh T1547.001
```

### 6. Análisis de Brechas
// turbo
```bash
python tools/custom-scripts/gap_analyzer.py --full-analysis --generate-recommendations
```

### 7. Generación de Reportes
// turbo
```bash
python tools/custom-scripts/purple_report.py --full-report
```

### 8. Revisión y Cierre
- Revisar resultados con el equipo
- Documentar lecciones aprendidas
- Crear tickets de mejora
- Programar siguiente ejercicio

## Escenarios Predefinidos

### credential-theft
Simulación de robo de credenciales:
- T1003.001 - LSASS Memory
- T1003.002 - SAM Database
- T1110.001 - Password Guessing

### lateral-movement
Simulación de movimiento lateral:
- T1021.001 - Remote Desktop
- T1021.002 - SMB Admin Shares
- T1021.006 - WinRM

### ransomware
Simulación de ransomware:
- T1486 - Data Encrypted for Impact
- T1490 - Inhibit System Recovery
- T1489 - Service Stop

### apt-simulation
Simulación de APT completa:
- T1566.001 - Spearphishing Attachment
- T1059.001 - PowerShell
- T1547.001 - Registry Run Keys
- T1003.001 - LSASS Memory
- T1021.002 - SMB Admin Shares
- T1048.003 - Exfiltration Over HTTP

## Parámetros

| Parámetro | Descripción | Requerido | Default |
|-----------|-------------|-----------|---------|
| --scenario | Escenario predefinido | No | - |
| --techniques | Lista de técnicas separadas por coma | No | - |
| --quick | Ejercicio rápido (3 técnicas) | No | false |
| --full | Ejercicio completo (todas las técnicas) | No | false |
| --report-only | Solo generar reporte | No | false |

## Ejemplo Completo

```
Usuario: /purple-exercise --scenario credential-theft

Windsurf AI:
🟣 PURPLE TEAM EXERCISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Escenario: Credential Theft
🎯 Técnicas: T1003.001, T1003.002, T1110.001
⏱️ Duración Estimada: 30 minutos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 FASE 1: SIMULACIÓN DE ATAQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/3] T1003.001 - LSASS Memory
      ⏳ Ejecutando... ✅ Completado (5s)
      📁 Evidencia: attacks/T1003.001/20240115_110000.yaml

[2/3] T1003.002 - SAM Database
      ⏳ Ejecutando... ✅ Completado (3s)
      📁 Evidencia: attacks/T1003.002/20240115_110005.yaml

[3/3] T1110.001 - Password Guessing
      ⏳ Ejecutando... ✅ Completado (10s)
      📁 Evidencia: attacks/T1110.001/20240115_110008.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 FASE 2: VALIDACIÓN DE DETECCIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/3] T1003.001 - LSASS Memory
      Sysmon: ✅ | EDR: ✅ | Sigma: ✅
      Cobertura: 90% | MTTD: 30s

[2/3] T1003.002 - SAM Database
      Sysmon: ✅ | EDR: ⚠️ | Sigma: ✅
      Cobertura: 70% | MTTD: 2m

[3/3] T1110.001 - Password Guessing
      Sysmon: ❌ | EDR: ✅ | Sigma: ⚠️
      Cobertura: 50% | MTTD: 5m

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟣 FASE 3: ANÁLISIS DE BRECHAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Brechas Identificadas: 2

🟠 T1003.002 - SAM Database
   Gap: EDR no generó alerta
   Recomendación: Configurar regla de acceso a SAM

🟡 T1110.001 - Password Guessing
   Gap: Detección lenta (5 min)
   Recomendación: Reducir umbral de alertas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RESUMEN DEL EJERCICIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│ Técnicas Probadas:        3                             │
│ Técnicas Detectadas:      3 (100%)                      │
│ Cobertura Promedio:       70%                           │
│ MTTD Promedio:            2.5 min                       │
│ Brechas Críticas:         0                             │
│ Brechas Altas:            1                             │
│ Brechas Medias:           1                             │
└─────────────────────────────────────────────────────────┘

Estado General: 🟡 BUENO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 REPORTES GENERADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• reports/executive_summary_20240115.md
• reports/exercises/exercise_report_20240115.md
• reports/gaps/gap_report_20240115.md
• reports/metrics/metrics_report_20240115.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 PLAN DE ACCIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| # | Técnica | Acción | Responsable | Fecha |
|---|---------|--------|-------------|-------|
| 1 | T1003.002 | Configurar EDR | Blue Team | +3d |
| 2 | T1110.001 | Ajustar umbral | Blue Team | +5d |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ EJERCICIO COMPLETADO

Próximo ejercicio sugerido: 2024-02-15
Enfoque: Validar correcciones implementadas
```

## Checklist Pre-Ejercicio

- [ ] Ambiente de pruebas disponible
- [ ] Herramientas instaladas y funcionando
- [ ] Equipo notificado
- [ ] Logs habilitados
- [ ] Plan de rollback definido
- [ ] Documentación lista

## Checklist Post-Ejercicio

- [ ] Resultados documentados
- [ ] Brechas identificadas
- [ ] Recomendaciones generadas
- [ ] Tickets creados
- [ ] Equipo debriefed
- [ ] Próximo ejercicio programado

## Notas

- Ejecutar en horario acordado
- Mantener comunicación con Blue Team
- Documentar cualquier incidente
- Preservar evidencia para análisis
