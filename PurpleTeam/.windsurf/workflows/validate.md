---
description: Validar detección de técnica ATT&CK en fuentes de seguridad
---

# /validate - Validación de Detección

Este workflow valida si una técnica ATT&CK fue detectada por los controles de seguridad.

## Uso

```
/validate T1003.001
/validate T1059.001 --timeframe 2h
/validate T1547.001 --source sigma
```

## Pasos del Workflow

### 1. Identificar Técnica
Obtener información de la técnica a validar.

```bash
python tools/custom-scripts/mitre_mapper.py --technique {TECHNIQUE_ID}
```

### 2. Definir Ventana de Tiempo
Establecer el período de tiempo para buscar detecciones:
- Default: última hora
- Ajustar según tiempo de ejecución del ataque

### 3. Verificar Reglas Sigma
// turbo
```bash
./tools/custom-scripts/detection_validate.sh {TECHNIQUE_ID} --source sigma
```

### 4. Verificar Eventos Sysmon
// turbo
```bash
./tools/custom-scripts/detection_validate.sh {TECHNIQUE_ID} --source sysmon
```

### 5. Verificar Alertas EDR
Consultar el EDR para alertas relacionadas:
- Buscar por técnica ATT&CK
- Buscar por indicadores específicos
- Verificar severidad de alertas

### 6. Verificar SIEM
Consultar el SIEM para eventos correlacionados:
- Buscar reglas que hayan disparado
- Verificar casos creados
- Revisar timeline de eventos

### 7. Calcular Cobertura
Determinar porcentaje de cobertura basado en:
- Número de fuentes que detectaron
- Tiempo de detección (MTTD)
- Calidad de las alertas

### 8. Documentar Resultado
// turbo
```bash
./tools/custom-scripts/detection_validate.sh {TECHNIQUE_ID} --timeframe 1h
```

## Parámetros

| Parámetro | Descripción | Requerido | Default |
|-----------|-------------|-----------|---------|
| TECHNIQUE_ID | ID de técnica ATT&CK | Sí | - |
| --timeframe | Ventana de tiempo (1h, 30m, 1d) | No | 1h |
| --source | Fuente específica a verificar | No | all |

## Fuentes de Detección

| Fuente | Descripción | Eventos Típicos |
|--------|-------------|-----------------|
| sysmon | Sysmon Event Logs | 1, 3, 7, 8, 10, 11, 13 |
| windows_security | Windows Security | 4624, 4688, 4656, 5140 |
| powershell | PowerShell Logging | 4103, 4104 |
| edr | Endpoint Detection | Alertas específicas |
| sigma | Sigma Rules | Reglas matching |
| yara | YARA Rules | Detecciones de malware |
| network | Network Traffic | Conexiones, DNS |

## Ejemplo Completo

```
Usuario: /validate T1003.001

Windsurf AI:
🔵 Validando detección para T1003.001

📋 Técnica: T1003.001 - LSASS Memory
📂 Táctica: Credential Access
⏰ Timeframe: última hora

🔍 Verificando fuentes de detección...

📊 Resultados:

┌─────────────────┬──────────┬─────────────────┐
│ Fuente          │ Estado   │ Tiempo          │
├─────────────────┼──────────┼─────────────────┤
│ Sigma Rules     │ ✅       │ -               │
│ Sysmon Event 10 │ ✅       │ 2 min           │
│ Windows Security│ ✅       │ 3 min           │
│ EDR Alert       │ ✅       │ 30 seg          │
│ Network         │ ⚪       │ N/A             │
└─────────────────┴──────────┴─────────────────┘

📈 Cobertura: 80%
⏱️ MTTD Promedio: 1.5 min

✅ Detección EXITOSA

📁 Resultado guardado en: detections/T1003.001/20240115_104530.yaml

📋 Siguiente paso:
   Si cobertura < 80%: /gap-analysis T1003.001
   Si cobertura >= 80%: Documentar y continuar
```

## Interpretación de Resultados

### Cobertura >= 80%
- ✅ Detección exitosa
- Documentar y mantener reglas
- Considerar optimización de tiempos

### Cobertura 50-79%
- ⚠️ Detección parcial
- Identificar fuentes faltantes
- Implementar reglas adicionales

### Cobertura < 50%
- ❌ Detección insuficiente
- Ejecutar gap analysis
- Priorizar implementación

## Notas

- Verificar que los logs estén habilitados
- Considerar latencia de replicación de logs
- Documentar falsos positivos encontrados
