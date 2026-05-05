---
description: Investigate security incident - Deep dive analysis workflow
---

# /investigate - Incident Investigation Workflow

Investigar un incidente de seguridad en profundidad.

## Uso
```
/investigate [incident_id|description]
```

## Ejemplos:
- `/investigate INC-2024-0001`
- `/investigate "conexiones sospechosas a IP externa"`
- `/investigate "usuario admin con actividad inusual"`

## Pasos del Workflow

### 1. Crear o cargar incidente
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --new "Descripción del incidente" -s high
```

### 2. Recolectar evidencia inicial
// turbo
```bash
cd ~/Documents/BlueTeam\ -\ KaliLinux && ./tools/custom-scripts/forensic_collector.sh --system --network --processes
```

### 3. Analizar logs relacionados
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/log_analyzer.py --analyze /var/log/auth.log --report investigation_report.md
```

### 4. Ejecutar threat hunting
```bash
cd ~/Documents/BlueTeam\ -\ KaliLinux && ./tools/custom-scripts/threat_hunter.sh --hunt-all
```

### 5. Correlacionar eventos
- Revisar timeline de eventos
- Identificar punto de entrada
- Mapear movimiento lateral
- Documentar técnicas usadas (MITRE ATT&CK)

### 6. Extraer IOCs
- IPs maliciosas
- Dominios sospechosos
- Hashes de archivos
- URLs de C2
- Guardar en `iocs/`

### 7. Generar reporte de investigación
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --report INC-XXXX-XXXX
```

## Checklist de Investigación

- [ ] Identificar vector de entrada inicial
- [ ] Determinar alcance del compromiso
- [ ] Identificar datos afectados
- [ ] Documentar timeline completo
- [ ] Extraer todos los IOCs
- [ ] Mapear a MITRE ATT&CK
- [ ] Identificar actor de amenaza (si es posible)
- [ ] Determinar impacto al negocio
- [ ] Preparar recomendaciones

## Preguntas Clave

1. **¿Qué pasó?** - Descripción del incidente
2. **¿Cuándo?** - Timeline de eventos
3. **¿Cómo?** - Vector de ataque y técnicas
4. **¿Quién?** - Actor de amenaza
5. **¿Qué se afectó?** - Sistemas y datos
6. **¿Sigue activo?** - Estado actual

## Output Esperado

```
📋 Investigation Report - INC-2024-0001
═══════════════════════════════════════════════════════════════

🎯 Incident Summary:
   Type: Intrusion
   Severity: HIGH
   Status: Investigating
   
📅 Timeline:
   • 2024-01-15 10:23 - Initial access via SSH brute force
   • 2024-01-15 10:45 - Privilege escalation to root
   • 2024-01-15 11:02 - Lateral movement to db-server
   • 2024-01-15 11:30 - Data exfiltration detected

🔍 IOCs:
   • Attacker IP: 45.33.32.156
   • Malware hash: a1b2c3d4...
   • C2 domain: evil-c2.com

🗺️ MITRE ATT&CK:
   • T1110 - Brute Force
   • T1548 - Abuse Elevation Control
   • T1021 - Remote Services
   • T1041 - Exfiltration Over C2

📊 Recommendations:
   1. Block attacker IP at perimeter
   2. Reset all credentials
   3. Isolate affected systems
   4. Deploy additional monitoring
```
