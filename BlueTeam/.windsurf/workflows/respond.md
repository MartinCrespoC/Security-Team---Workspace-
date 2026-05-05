---
description: Respond to security incident - Containment and remediation workflow
---

# /respond - Incident Response Workflow

Responder y contener un incidente de seguridad activo.

## Uso
```
/respond [action] [target]
```

## Acciones disponibles:
- `contain` - Contener amenaza
- `block` - Bloquear IP/dominio
- `isolate` - Aislar host
- `kill` - Terminar proceso
- `disable` - Deshabilitar usuario
- `collect` - Recolectar evidencia

## Ejemplos:
- `/respond contain 192.168.1.100`
- `/respond block malicious.com`
- `/respond isolate`
- `/respond kill 1234`
- `/respond disable compromised_user`

## Pasos del Workflow

### 1. Evaluar la situación
- Confirmar que es un incidente real
- Determinar severidad
- Identificar sistemas afectados

### 2. Contención inmediata

#### Bloquear IP maliciosa:
// turbo
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --contain --ip <IP_ADDRESS>
```

#### Matar proceso malicioso:
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --contain --pid <PID>
```

#### Deshabilitar usuario comprometido:
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --contain --user <USERNAME>
```

#### Bloquear dominio:
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --contain --domain <DOMAIN>
```

#### Aislar host completamente:
```bash
python3 ~/Documents/BlueTeam\ -\ KaliLinux/tools/custom-scripts/incident_response.py --isolate
```

### 3. Preservar evidencia
```bash
cd ~/Documents/BlueTeam\ -\ KaliLinux && ./tools/custom-scripts/forensic_collector.sh --collect-all --package
```

### 4. Documentar acciones
Registrar todas las acciones tomadas en el incidente:
- Hora de la acción
- Qué se hizo
- Por qué se hizo
- Resultado

### 5. Verificar contención
- Confirmar que la amenaza está contenida
- Verificar que no hay más actividad maliciosa
- Monitorear sistemas afectados

### 6. Comunicar
- Notificar a stakeholders relevantes
- Actualizar estado del incidente
- Preparar comunicación si es necesario

## Matriz de Respuesta por Severidad

| Severidad | Tiempo Respuesta | Acciones |
|-----------|------------------|----------|
| CRITICAL | < 15 min | Aislar, bloquear, escalar |
| HIGH | < 1 hora | Contener, investigar |
| MEDIUM | < 4 horas | Analizar, documentar |
| LOW | < 24 horas | Monitorear, revisar |

## Comandos de Contención Rápida

### Bloquear IP con iptables:
```bash
sudo iptables -A INPUT -s <IP> -j DROP
sudo iptables -A OUTPUT -d <IP> -j DROP
```

### Matar proceso y sus hijos:
```bash
sudo pkill -9 -P <PID>
sudo kill -9 <PID>
```

### Deshabilitar cuenta:
```bash
sudo usermod -L <username>
sudo chage -E 0 <username>
```

### Bloquear dominio:
```bash
echo "127.0.0.1 <domain>" | sudo tee -a /etc/hosts
```

## Checklist de Respuesta

- [ ] Incidente confirmado
- [ ] Severidad determinada
- [ ] Sistemas afectados identificados
- [ ] Contención ejecutada
- [ ] Evidencia preservada
- [ ] Acciones documentadas
- [ ] Stakeholders notificados
- [ ] Monitoreo aumentado

## Output Esperado

```
🚨 Incident Response Actions
═══════════════════════════════════════════════════════════════

📋 Incident: INC-2024-0001
⚡ Severity: CRITICAL
🕐 Response Time: 3 minutes

✅ Actions Taken:
   1. [10:23:45] Blocked IP 45.33.32.156 via iptables
   2. [10:24:12] Killed process 1234 (nc -e /bin/bash)
   3. [10:25:01] Disabled user 'compromised_admin'
   4. [10:26:30] Collected forensic evidence

📊 Status: CONTAINED
   • Malicious connections: Blocked
   • Malicious processes: Terminated
   • Compromised accounts: Disabled

🔍 Next Steps:
   1. Complete forensic analysis
   2. Identify root cause
   3. Remediate vulnerabilities
   4. Restore normal operations
```
