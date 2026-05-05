---
description: Simular técnica MITRE ATT&CK para validación de controles
---

# /simulate - Simulación de Técnica ATT&CK

Este workflow ejecuta una simulación de ataque basada en MITRE ATT&CK para validar controles de seguridad.

## Uso

```
/simulate T1003.001
/simulate T1059.001 --tool atomic
/simulate T1547.001 --dry-run
```

## Pasos del Workflow

### 1. Validar Técnica
Verificar que el ID de técnica proporcionado es válido en MITRE ATT&CK.

```bash
python tools/custom-scripts/attack_simulate.py --technique {TECHNIQUE_ID} --dry-run
```

### 2. Preparar Ambiente
Asegurar que el ambiente de pruebas está listo:
- Verificar que las herramientas necesarias están instaladas
- Confirmar que el sistema objetivo está disponible
- Iniciar captura de logs

### 3. Ejecutar Simulación
// turbo
```bash
python tools/custom-scripts/attack_simulate.py --technique {TECHNIQUE_ID} --tool atomic
```

### 4. Capturar Evidencia
Documentar la ejecución:
- Timestamp de inicio y fin
- Comandos ejecutados
- Artefactos generados
- Screenshots si aplica

### 5. Verificar Detección Inicial
Ejecutar validación rápida de detección:

```bash
./tools/custom-scripts/detection_validate.sh {TECHNIQUE_ID} --timeframe 5m
```

### 6. Documentar Resultado
Guardar resultado en `attacks/{TECHNIQUE_ID}/`:
- Archivo YAML con detalles de ejecución
- Logs capturados
- Estado de detección inicial

## Parámetros

| Parámetro | Descripción | Requerido | Default |
|-----------|-------------|-----------|---------|
| TECHNIQUE_ID | ID de técnica ATT&CK (ej: T1003.001) | Sí | - |
| --tool | Herramienta a usar (atomic, caldera, custom) | No | atomic |
| --dry-run | Mostrar comando sin ejecutar | No | false |
| --target | Sistema objetivo (local, remote) | No | local |

## Técnicas Comunes

### Credential Access
- `T1003.001` - LSASS Memory Dump
- `T1003.002` - SAM Database
- `T1003.003` - NTDS

### Execution
- `T1059.001` - PowerShell
- `T1059.003` - Windows Command Shell
- `T1059.004` - Unix Shell

### Persistence
- `T1547.001` - Registry Run Keys
- `T1053.005` - Scheduled Task

### Defense Evasion
- `T1055.001` - DLL Injection
- `T1070.001` - Clear Event Logs

## Ejemplo Completo

```
Usuario: /simulate T1003.001

Windsurf AI:
🔴 Iniciando simulación de técnica ATT&CK

📋 Técnica: T1003.001 - LSASS Memory
📂 Táctica: Credential Access
🔧 Herramienta: Atomic Red Team

⏳ Ejecutando simulación...
   Comando: Invoke-AtomicTest T1003.001
   
✅ Simulación completada
   Timestamp: 2024-01-15 10:30:45
   Duración: 5 segundos
   Artefactos: lsass.dmp

📊 Verificación inicial de detección:
   - Sysmon Event 10: ✅ Detectado
   - EDR Alert: ⏳ Pendiente
   
📁 Resultado guardado en: attacks/T1003.001/20240115_103045.yaml

📋 Siguiente paso:
   Ejecutar: /validate T1003.001
   Para validación completa de detección
```

## Notas de Seguridad

- Solo ejecutar en sistemas autorizados
- Documentar todas las acciones
- Tener plan de rollback
- Notificar al equipo antes de ejercicios
