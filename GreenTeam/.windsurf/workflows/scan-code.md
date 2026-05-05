---
description: Escaneo completo de seguridad del código fuente usando SAST
---

# 🔍 /scan-code - Escaneo de Código Fuente

Este workflow ejecuta un análisis estático de seguridad (SAST) completo del código.

## Pasos

1. **Detectar lenguajes del proyecto**
   - Identificar archivos Python (.py)
   - Identificar archivos JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
   - Identificar archivos Go (.go)
   - Identificar archivos Java (.java)
   - Identificar archivos Ruby (.rb)
   - Identificar archivos PHP (.php)

2. **Ejecutar Semgrep (multi-lenguaje)**
   ```bash
   semgrep scan --config auto . --json > scans/sast/semgrep.json
   ```
   // turbo

3. **Ejecutar Bandit (si hay Python)**
   ```bash
   bandit -r . -f json -o scans/sast/bandit.json
   ```
   // turbo

4. **Ejecutar ESLint Security (si hay JavaScript)**
   ```bash
   eslint . --ext .js,.ts,.jsx,.tsx --plugin security -f json > scans/sast/eslint.json
   ```

5. **Ejecutar Gosec (si hay Go)**
   ```bash
   gosec -fmt=json -out=scans/sast/gosec.json ./...
   ```

6. **Generar reporte consolidado**
   - Combinar resultados de todas las herramientas
   - Clasificar por severidad (Critical, High, Medium, Low)
   - Mapear a CWE/OWASP

7. **Mostrar resumen de vulnerabilidades**
   - Tabla con vulnerabilidades encontradas
   - Sugerencias de fix para cada una
   - Referencias a documentación

## Uso Alternativo

Ejecutar el script directamente:
```bash
./tools/custom-scripts/secure_scan.sh <directorio>
```

## Output Esperado

```
## 🔍 Análisis de Seguridad

### Vulnerabilidades Detectadas
| Severidad | Tipo | Archivo | Línea | Descripción |
|-----------|------|---------|-------|-------------|
| 🔴 Critical | SQL Injection | app.py | 45 | User input in SQL query |
| 🟠 High | XSS | index.js | 123 | innerHTML with user data |

### 🛠️ Fixes Sugeridos
[Código corregido para cada vulnerabilidad]

### 📊 Resumen
- **Críticas:** 1
- **Altas:** 1
- **Medias:** 3
- **Bajas:** 5
```

## Herramientas Utilizadas

| Herramienta | Lenguajes | Descripción |
|-------------|-----------|-------------|
| Semgrep | Multi | Scanner SAST rápido y extensible |
| Bandit | Python | Análisis de seguridad para Python |
| ESLint Security | JS/TS | Reglas de seguridad para JavaScript |
| Gosec | Go | Security checker para Go |
| Brakeman | Ruby | Scanner para Ruby on Rails |

## Security Gates

- ❌ **FAIL** si hay vulnerabilidades críticas
- ⚠️ **WARN** si hay más de 5 vulnerabilidades altas
- ✅ **PASS** en caso contrario
