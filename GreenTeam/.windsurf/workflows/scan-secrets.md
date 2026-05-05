---
description: Buscar secrets y credenciales expuestas en el código
---

# 🔑 /scan-secrets - Detección de Secrets

Este workflow busca secrets, credenciales y tokens expuestos en el código.

## Pasos

1. **Ejecutar Gitleaks**
   ```bash
   gitleaks detect --source . --report-format json --report-path scans/secrets/gitleaks.json --no-git
   ```
   // turbo

2. **Ejecutar TruffleHog**
   ```bash
   trufflehog filesystem . --json > scans/secrets/trufflehog.json
   ```
   // turbo

3. **Ejecutar detect-secrets**
   ```bash
   detect-secrets scan . > scans/secrets/detect-secrets.json
   ```
   // turbo

4. **Buscar patrones personalizados**
   - API Keys
   - Passwords hardcodeados
   - Tokens de acceso
   - Claves privadas
   - Connection strings

5. **Generar reporte**

## Uso Alternativo

```bash
./tools/custom-scripts/secret_scanner.sh <directorio>
```

## Patrones Detectados

| Tipo | Patrón | Severidad |
|------|--------|-----------|
| AWS Keys | `AKIA[0-9A-Z]{16}` | 🔴 Critical |
| Private Keys | `-----BEGIN.*PRIVATE KEY-----` | 🔴 Critical |
| API Keys | `api[_-]?key.*=.*` | 🟠 High |
| Passwords | `password.*=.*` | 🟠 High |
| Tokens | `token.*=.*` | 🟠 High |
| Connection Strings | `mongodb://.*:.*@` | 🟠 High |

## Security Gate

- ❌ **FAIL** si se encuentra cualquier secret
- ✅ **PASS** si no hay secrets expuestos

## Acciones Requeridas

1. **Rotar credenciales** comprometidas inmediatamente
2. **Remover secrets** del código
3. **Usar variables de entorno** o secret managers
4. **Revisar historial de git** para exposición previa
