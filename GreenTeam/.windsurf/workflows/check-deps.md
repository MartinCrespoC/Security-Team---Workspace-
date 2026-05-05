---
description: Verificar dependencias por vulnerabilidades conocidas (SCA)
---

# 📦 /check-deps - Verificación de Dependencias

Este workflow ejecuta un análisis de composición de software (SCA) para detectar vulnerabilidades en dependencias.

## Pasos

1. **Detectar ecosistemas de dependencias**
   - Python: requirements.txt, Pipfile, pyproject.toml
   - Node.js: package.json, package-lock.json, yarn.lock
   - Ruby: Gemfile, Gemfile.lock
   - Go: go.mod, go.sum
   - Java: pom.xml, build.gradle
   - Rust: Cargo.toml
   - PHP: composer.json

2. **Ejecutar Safety (Python)**
   ```bash
   safety check -r requirements.txt --json > scans/sca/safety.json
   ```
   // turbo

3. **Ejecutar pip-audit (Python)**
   ```bash
   pip-audit -r requirements.txt --format json > scans/sca/pip-audit.json
   ```
   // turbo

4. **Ejecutar npm audit (Node.js)**
   ```bash
   npm audit --json > scans/sca/npm-audit.json
   ```
   // turbo

5. **Ejecutar Snyk (multi-ecosistema)**
   ```bash
   snyk test --json > scans/sca/snyk.json
   ```

6. **Ejecutar OWASP Dependency-Check**
   ```bash
   dependency-check.sh --scan . --format JSON --out scans/sca/
   ```

7. **Generar reporte de vulnerabilidades**
   - Listar paquetes vulnerables
   - Mostrar versiones afectadas
   - Indicar versiones corregidas
   - Incluir CVEs y referencias

8. **Mostrar resumen y recomendaciones**

## Uso Alternativo

Ejecutar el script directamente:
```bash
python tools/custom-scripts/dependency_check.py <directorio>
```

## Output Esperado

```
## 📦 Dependency Security Report

### Vulnerabilidades en Dependencias
| Package | Version | Severity | CVE | Fix Version |
|---------|---------|----------|-----|-------------|
| lodash | 4.17.15 | 🔴 Critical | CVE-2021-23337 | 4.17.21 |
| axios | 0.21.0 | 🟠 High | CVE-2021-3749 | 0.21.2 |

### 📊 Resumen
- **Críticas:** 1
- **Altas:** 1
- **Medias:** 3
- **Bajas:** 2

### 🛠️ Comandos de Actualización
```bash
npm update lodash axios
pip install --upgrade requests
```
```

## Herramientas Utilizadas

| Herramienta | Ecosistema | Descripción |
|-------------|------------|-------------|
| Safety | Python | Verificación de dependencias Python |
| pip-audit | Python | Auditoría de paquetes pip |
| npm audit | Node.js | Auditoría de paquetes npm |
| Snyk | Multi | Análisis de dependencias multi-plataforma |
| OWASP DC | Multi | Detección de CVEs en dependencias |
| RetireJS | JavaScript | Scanner de librerías JavaScript |

## Security Gates

- ❌ **FAIL** si hay dependencias con vulnerabilidades críticas
- ⚠️ **WARN** si hay más de 5 vulnerabilidades altas
- ✅ **PASS** en caso contrario

## Acciones Automáticas

1. Generar PR con actualizaciones de dependencias
2. Crear issues para vulnerabilidades críticas
3. Notificar al equipo de seguridad
