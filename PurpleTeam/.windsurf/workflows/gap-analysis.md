---
description: Analizar brechas de detección y generar recomendaciones
---

# /gap-analysis - Análisis de Brechas

Este workflow analiza las brechas de detección identificadas y genera recomendaciones de mejora.

## Uso

```
/gap-analysis
/gap-analysis T1003.001
/gap-analysis --tactic "Credential Access"
/gap-analysis --generate-recommendations
```

## Pasos del Workflow

### 1. Recolectar Datos
Obtener información de ataques y detecciones ejecutadas.

// turbo
```bash
python tools/custom-scripts/gap_analyzer.py --full-analysis
```

### 2. Identificar Técnicas sin Cobertura
Listar técnicas que no fueron detectadas o tienen cobertura insuficiente.

### 3. Clasificar por Severidad
Priorizar brechas según:
- Impacto potencial de la técnica
- Frecuencia de uso por adversarios
- Facilidad de implementación de detección

### 4. Analizar Causas Raíz
Para cada brecha identificar:
- ¿Falta regla de detección?
- ¿Regla existe pero no está habilitada?
- ¿Logs no están siendo recolectados?
- ¿Falso negativo en regla existente?

### 5. Generar Recomendaciones
// turbo
```bash
python tools/custom-scripts/gap_analyzer.py --generate-recommendations
```

### 6. Crear Plan de Remediación
Documentar acciones específicas:
- Reglas Sigma a implementar
- Configuraciones de logging a habilitar
- Alertas de EDR a crear

### 7. Exportar Reporte
Guardar análisis en `gaps/analysis/`:
- Reporte completo en Markdown
- Datos en YAML para tracking
- Reglas sugeridas

## Parámetros

| Parámetro | Descripción | Requerido | Default |
|-----------|-------------|-----------|---------|
| TECHNIQUE_ID | Analizar técnica específica | No | all |
| --tactic | Filtrar por táctica | No | - |
| --full-analysis | Análisis completo | No | false |
| --generate-recommendations | Generar recomendaciones | No | false |

## Severidades

| Severidad | Descripción | Acción |
|-----------|-------------|--------|
| 🔴 Crítica | Técnica de alto impacto sin detección | Inmediata |
| 🟠 Alta | Técnica común sin cobertura adecuada | Esta semana |
| 🟡 Media | Cobertura parcial, mejoras necesarias | Este mes |
| 🔵 Baja | Optimizaciones menores | Backlog |

## Ejemplo Completo

```
Usuario: /gap-analysis

Windsurf AI:
🟣 Analizando brechas de detección...

📊 Resumen de Análisis:

┌────────────────────────────────────────────────┐
│ Total Técnicas Analizadas: 15                  │
│ Técnicas con Brechas: 5                        │
│ Brechas Críticas: 1                            │
│ Brechas Altas: 2                               │
│ Brechas Medias: 2                              │
│ Cobertura General: 65%                         │
└────────────────────────────────────────────────┘

🔴 BRECHAS CRÍTICAS:

┌─────────────────────────────────────────────────────────┐
│ T1055.001 - DLL Injection                               │
├─────────────────────────────────────────────────────────┤
│ Cobertura: 0%                                           │
│ Fuentes Faltantes: sysmon, edr, sigma                   │
│                                                         │
│ Recomendaciones:                                        │
│ 1. Implementar regla Sigma para CreateRemoteThread      │
│ 2. Habilitar Sysmon Event 8                             │
│ 3. Configurar alerta EDR para process injection         │
│                                                         │
│ Regla Sigma Sugerida:                                   │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ title: CreateRemoteThread API Call                  │ │
│ │ logsource:                                          │ │
│ │   category: create_remote_thread                    │ │
│ │   product: windows                                  │ │
│ │ detection:                                          │ │
│ │   selection:                                        │ │
│ │     EventType: CreateRemoteThread                   │ │
│ │   condition: selection                              │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

🟠 BRECHAS ALTAS:

• T1070.001 - Clear Windows Event Logs (Cobertura: 40%)
  → Habilitar auditoría de Event Log clearing

• T1021.002 - SMB/Windows Admin Shares (Cobertura: 35%)
  → Implementar monitoreo de acceso a admin shares

📋 Plan de Acción:

| # | Técnica | Acción | Prioridad | Responsable |
|---|---------|--------|-----------|-------------|
| 1 | T1055.001 | Implementar regla Sigma | Crítica | Blue Team |
| 2 | T1070.001 | Habilitar auditoría | Alta | Blue Team |
| 3 | T1021.002 | Configurar monitoreo | Alta | Blue Team |

📁 Reporte guardado en: gaps/analysis/gap_analysis_20240115.yaml
📁 Recomendaciones en: gaps/recommendations/recommendations_20240115.md

📋 Siguiente paso:
   Implementar correcciones y ejecutar: /purple-exercise
   Para validar las mejoras
```

## Tipos de Brechas

### NO_DETECTION
- No existe ninguna detección para la técnica
- Requiere implementación completa

### PARTIAL_DETECTION
- Algunas fuentes detectan, otras no
- Requiere completar cobertura

### DELAYED_DETECTION
- Detección existe pero es lenta
- Requiere optimización de reglas

### HIGH_FALSE_POSITIVES
- Detección genera muchos falsos positivos
- Requiere tuning de reglas

### NO_RULE
- Logs existen pero no hay regla
- Requiere crear regla de detección

## Notas

- Priorizar técnicas usadas por adversarios relevantes
- Considerar threat intelligence al priorizar
- Documentar justificación de excepciones
