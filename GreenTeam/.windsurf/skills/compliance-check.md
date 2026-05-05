---
description: Skill para verificar compliance con estándares de seguridad
---

# 📋 Compliance Check Skill

## Descripción

Este skill verifica el cumplimiento del código y la infraestructura con estándares de seguridad y regulaciones de la industria.

## Frameworks Soportados

### OWASP Top 10 (2021)

| ID | Categoría | Verificación |
|----|-----------|--------------|
| A01 | Broken Access Control | Verificar autorización en endpoints |
| A02 | Cryptographic Failures | Verificar algoritmos y configuración |
| A03 | Injection | Verificar sanitización de inputs |
| A04 | Insecure Design | Revisar arquitectura de seguridad |
| A05 | Security Misconfiguration | Verificar configuraciones |
| A06 | Vulnerable Components | Verificar dependencias |
| A07 | Auth Failures | Verificar autenticación |
| A08 | Software Integrity | Verificar integridad de código |
| A09 | Logging Failures | Verificar logging de seguridad |
| A10 | SSRF | Verificar validación de URLs |

### CWE Top 25 (2023)

| Rank | CWE | Descripción |
|------|-----|-------------|
| 1 | CWE-787 | Out-of-bounds Write |
| 2 | CWE-79 | Cross-site Scripting |
| 3 | CWE-89 | SQL Injection |
| 4 | CWE-416 | Use After Free |
| 5 | CWE-78 | OS Command Injection |
| 6 | CWE-20 | Improper Input Validation |
| 7 | CWE-125 | Out-of-bounds Read |
| 8 | CWE-22 | Path Traversal |
| 9 | CWE-352 | CSRF |
| 10 | CWE-434 | Unrestricted Upload |

### PCI DSS v4.0

| Requisito | Descripción | Checks |
|-----------|-------------|--------|
| 3.4 | Proteger datos de tarjetas | Encriptación, tokenización |
| 6.2 | Desarrollo seguro | SAST, code review |
| 6.3 | Vulnerabilidades conocidas | SCA, patching |
| 8.3 | Autenticación fuerte | MFA, password policy |
| 10.1 | Logging | Audit trails |

### HIPAA

| Sección | Requisito | Verificación |
|---------|-----------|--------------|
| 164.312(a) | Access Control | Autenticación, autorización |
| 164.312(b) | Audit Controls | Logging, monitoreo |
| 164.312(c) | Integrity | Checksums, firmas |
| 164.312(d) | Authentication | MFA, tokens |
| 164.312(e) | Transmission Security | TLS, encriptación |

### SOC 2 Type II

| Trust Principle | Criterios |
|-----------------|-----------|
| Security | Firewall, IDS, encryption |
| Availability | Redundancy, DR, backups |
| Processing Integrity | Input validation, error handling |
| Confidentiality | Access control, encryption |
| Privacy | Data minimization, consent |

## Formato de Reporte

```markdown
# 📋 Compliance Report

## Resumen Ejecutivo

| Framework | Cumplimiento | Estado |
|-----------|--------------|--------|
| OWASP Top 10 | 85% | ⚠️ |
| CWE Top 25 | 90% | ✅ |
| PCI DSS | 75% | ❌ |

## Hallazgos por Framework

### OWASP Top 10

#### A03:2021 - Injection ❌
- **Estado:** No cumple
- **Hallazgo:** SQL Injection en `app/database.py:45`
- **Remediación:** Usar queries parametrizadas
- **Prioridad:** Alta

#### A07:2021 - Auth Failures ⚠️
- **Estado:** Parcial
- **Hallazgo:** No hay rate limiting en login
- **Remediación:** Implementar rate limiting
- **Prioridad:** Media

### PCI DSS

#### Requisito 3.4 - Protección de datos ❌
- **Estado:** No cumple
- **Hallazgo:** Datos de tarjeta en logs
- **Remediación:** Implementar masking
- **Prioridad:** Crítica

## Plan de Remediación

| Prioridad | Hallazgo | Deadline |
|-----------|----------|----------|
| 🔴 Crítica | PCI 3.4 - Datos en logs | 24h |
| 🟠 Alta | OWASP A03 - SQL Injection | 48h |
| 🟡 Media | OWASP A07 - Rate limiting | 1 semana |
```

## Checks Automáticos

### Código
```bash
# OWASP checks
semgrep --config p/owasp-top-ten

# CWE checks
semgrep --config p/cwe-top-25
```

### Infraestructura
```bash
# PCI DSS
checkov -d . --framework pci_dss

# HIPAA
checkov -d . --framework hipaa

# SOC 2
checkov -d . --framework soc2
```

### Dependencias
```bash
# CVE checks
snyk test --severity-threshold=high
```

## Uso

1. Identificar frameworks aplicables al proyecto
2. Ejecutar checks automáticos
3. Revisar hallazgos manualmente
4. Generar reporte de compliance
5. Crear plan de remediación
6. Verificar correcciones
