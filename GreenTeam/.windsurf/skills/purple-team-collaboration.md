---
description: Skill para colaboración Purple Team entre Red Team y Blue Team
---

# 💜 Purple Team Collaboration Skill

## Descripción

Este skill facilita la colaboración entre equipos ofensivos (Red Team) y defensivos (Blue/Green Team) para mejorar la postura de seguridad de forma continua.

## Modelo de Colaboración

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PURPLE TEAM                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────┐                              ┌─────────────┐          │
│   │  🔴 RED     │◄────── Feedback Loop ───────►│  🟢 GREEN   │          │
│   │   TEAM      │                              │    TEAM     │          │
│   ├─────────────┤                              ├─────────────┤          │
│   │ • Exploits  │                              │ • Detection │          │
│   │ • Bypasses  │                              │ • Prevention│          │
│   │ • TTPs      │                              │ • Response  │          │
│   │ • Payloads  │                              │ • Hardening │          │
│   └─────────────┘                              └─────────────┘          │
│         │                                              │                 │
│         └──────────────────┬───────────────────────────┘                 │
│                            │                                             │
│                    ┌───────▼───────┐                                     │
│                    │   💜 PURPLE   │                                     │
│                    │   EXERCISES   │                                     │
│                    └───────────────┘                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Flujo de Trabajo

### 1. Red Team → Green Team

**Información compartida:**
- Vulnerabilidades explotadas exitosamente
- Técnicas de bypass utilizadas
- Payloads efectivos
- Rutas de ataque
- Indicadores de compromiso (IoCs)

**Formato de reporte:**
```markdown
## 🔴 Red Team Finding

**ID:** RT-2024-001
**Fecha:** 2024-05-04
**Técnica:** SQL Injection
**MITRE ATT&CK:** T1190

### Vector de Ataque
```
POST /api/login
Content-Type: application/json

{"username": "admin' OR '1'='1", "password": "x"}
```

### Impacto
- Bypass de autenticación
- Acceso a datos de usuarios
- Escalación de privilegios

### Evidencia
[Screenshots, logs, etc.]

### Recomendaciones
1. Implementar queries parametrizadas
2. Agregar WAF rules
3. Mejorar logging
```

### 2. Green Team → Red Team

**Información compartida:**
- Nuevas detecciones implementadas
- Controles de seguridad agregados
- Reglas de WAF/IDS
- Políticas de seguridad
- Métricas de detección

**Formato de reporte:**
```markdown
## 🟢 Green Team Response

**ID:** GT-2024-001
**En respuesta a:** RT-2024-001
**Fecha:** 2024-05-05

### Controles Implementados

1. **Código corregido**
   - Queries parametrizadas en todos los endpoints
   - Validación de input con whitelist

2. **Detección**
   - Regla Semgrep para SQL Injection
   - Alerta en SIEM para patrones sospechosos

3. **Prevención**
   - WAF rule para bloquear payloads SQL
   - Rate limiting en endpoint de login

### Métricas
- Tiempo de detección: < 1 minuto
- Tiempo de bloqueo: Inmediato
- False positives: 0.1%

### Solicitud de Re-test
Por favor validar que los controles son efectivos.
```

### 3. Purple Team Exercise

**Ejercicio conjunto:**
```markdown
## 💜 Purple Team Exercise

**Objetivo:** Validar detección de SQL Injection
**Fecha:** 2024-05-06
**Participantes:** Red Team, Green Team, SOC

### Escenario
1. Red Team ejecuta ataques de SQL Injection
2. Green Team monitorea detecciones
3. SOC valida alertas y respuesta

### Resultados

| Ataque | Detectado | Bloqueado | Tiempo |
|--------|-----------|-----------|--------|
| Basic SQLi | ✅ | ✅ | 0.5s |
| Encoded SQLi | ✅ | ✅ | 0.8s |
| Time-based SQLi | ✅ | ⚠️ | 2.1s |
| Second-order SQLi | ❌ | ❌ | N/A |

### Gaps Identificados
- Second-order SQL Injection no detectado
- Time-based SQLi no bloqueado inmediatamente

### Acciones
1. Agregar detección para second-order SQLi
2. Mejorar reglas de WAF para time-based
3. Re-test en 1 semana
```

## Métricas de Colaboración

### KPIs
| Métrica | Target | Actual |
|---------|--------|--------|
| MTTD (Mean Time to Detect) | < 5 min | 3.2 min |
| MTTR (Mean Time to Respond) | < 1 hour | 45 min |
| Detection Rate | > 95% | 92% |
| False Positive Rate | < 5% | 3.1% |
| Vulnerabilities Fixed | 100% | 98% |

### Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│                    Purple Team Dashboard                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Findings This Month        Detection Coverage                   │
│  ┌────────────────┐         ┌────────────────┐                  │
│  │ 🔴 Critical: 2 │         │ ████████░░ 85% │                  │
│  │ 🟠 High: 8     │         └────────────────┘                  │
│  │ 🟡 Medium: 15  │                                              │
│  │ 🔵 Low: 23     │         Response Time                        │
│  └────────────────┘         ┌────────────────┐                  │
│                             │ Avg: 45 min    │                  │
│  Exercises Completed: 12    │ Best: 5 min    │                  │
│  Gaps Closed: 45            │ Worst: 4 hours │                  │
│                             └────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Integración con Herramientas

### MITRE ATT&CK Mapping
```yaml
technique: T1190  # Exploit Public-Facing Application
subtechnique: T1190.001
tactic: Initial Access
detection:
  - Semgrep rule: sql-injection
  - WAF rule: sqli-block
  - SIEM alert: suspicious-query
mitigation:
  - M1050: Exploit Protection
  - M1026: Privileged Account Management
```

### Threat Intelligence
```yaml
ioc:
  type: pattern
  value: "' OR '1'='1"
  confidence: high
  source: internal-red-team
  first_seen: 2024-05-04
  tags:
    - sql-injection
    - authentication-bypass
```

## Uso

1. **Red Team** reporta hallazgos usando el formato estándar
2. **Green Team** implementa controles y reporta respuesta
3. **Purple Team** coordina ejercicios de validación
4. **Métricas** se actualizan automáticamente
5. **Gaps** se priorizan y remedian
6. **Ciclo** se repite continuamente
