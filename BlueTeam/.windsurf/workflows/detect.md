---
description: Detect threats in logs and system - Automated threat detection workflow
---

# /detect - Threat Detection Workflow

Detectar amenazas automáticamente en logs y sistema.

## Uso
```
/detect [target]
```

## Targets válidos:
- `system` - Escaneo completo del sistema
- `network` - Análisis de red
- `logs` - Análisis de logs
- `auth` - Logs de autenticación
- `<filepath>` - Archivo específico

## Pasos del Workflow

### 1. Identificar el target
Determinar qué se va a analizar basado en el input del usuario.

### 2. Ejecutar detección
// turbo
```bash
cd ~/Documents/BlueTeam\ -\ KaliLinux && ./tools/custom-scripts/detect.sh --full
```

### 3. Analizar logs específicos (si aplica)
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/log_analyzer.py --analyze <logfile>
```

### 4. Revisar resultados
- Leer el archivo de log generado en `logs/`
- Revisar alertas en `alerts/`
- Identificar IOCs encontrados

### 5. Generar reporte
Si se encuentran amenazas:
1. Crear alerta en `alerts/<severity>/`
2. Documentar IOCs en `iocs/`
3. Mapear a MITRE ATT&CK
4. Recomendar acciones

## Acciones Automáticas

Cuando detecte amenaza CRÍTICA:
1. Generar alerta inmediata
2. Recolectar evidencia
3. Proponer contención
4. Notificar al analista

## Ejemplo de Output

```
🔍 Threat Detection Results
═══════════════════════════════════════════════════════════════

📊 Summary:
   • Lines analyzed: 15,432
   • Threats detected: 3
   • Severity: 1 Critical, 2 High

🚨 Critical Findings:
   • Brute force attack from 192.168.1.100 (500+ attempts)
   • Suspicious process: nc -e /bin/bash

🎯 IOCs Extracted:
   • IP: 192.168.1.100
   • Process: nc -e /bin/bash

📋 Recommendations:
   1. Block IP 192.168.1.100
   2. Kill suspicious process
   3. Review affected accounts
```
