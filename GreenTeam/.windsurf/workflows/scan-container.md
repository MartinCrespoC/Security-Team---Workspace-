---
description: Escanear imagen Docker o Dockerfile por vulnerabilidades
---

# 🐳 /scan-container - Escaneo de Containers

Este workflow ejecuta un análisis de seguridad completo para containers Docker.

## Pasos

1. **Identificar target**
   - Si es imagen Docker: escanear imagen
   - Si es Dockerfile: analizar configuración
   - Si es directorio: buscar Dockerfiles

2. **Ejecutar Hadolint (Dockerfile linting)**
   ```bash
   hadolint Dockerfile --format json > scans/containers/hadolint.json
   ```
   // turbo

3. **Ejecutar Trivy (vulnerabilidades de imagen)**
   ```bash
   trivy image <imagen> --format json > scans/containers/trivy.json
   ```
   // turbo

4. **Ejecutar Grype (análisis de vulnerabilidades)**
   ```bash
   grype <imagen> -o json > scans/containers/grype.json
   ```
   // turbo

5. **Ejecutar Dockle (best practices)**
   ```bash
   dockle <imagen> -f json > scans/containers/dockle.json
   ```

6. **Generar SBOM con Syft**
   ```bash
   syft <imagen> -o json > scans/containers/sbom.json
   ```

7. **Analizar resultados**
   - Vulnerabilidades en imagen base
   - Paquetes desactualizados
   - Configuraciones inseguras
   - Secrets en capas

8. **Generar reporte y recomendaciones**

## Uso

```bash
# Escanear imagen
/scan-container nginx:latest

# Escanear Dockerfile
/scan-container ./Dockerfile

# Escanear directorio con Dockerfiles
/scan-container ./docker/
```

## Uso Alternativo

Ejecutar el script directamente:
```bash
./tools/custom-scripts/container_scan.sh -i <imagen>
./tools/custom-scripts/container_scan.sh -f <Dockerfile>
./tools/custom-scripts/container_scan.sh -d <directorio>
```

## Output Esperado

```
## 🐳 Container Security Report

### Imagen: nginx:latest

### Vulnerabilidades
| Severidad | Package | Version | CVE | Fix |
|-----------|---------|---------|-----|-----|
| 🔴 Critical | openssl | 1.1.1k | CVE-2021-3711 | 1.1.1l |
| 🟠 High | curl | 7.74.0 | CVE-2021-22945 | 7.79.0 |

### Dockerfile Issues
| Severidad | Código | Descripción |
|-----------|--------|-------------|
| 🟠 Warning | DL3007 | Using latest tag |
| 🟡 Info | DL3008 | Pin versions in apt-get |

### Best Practices
- ❌ Running as root
- ❌ No HEALTHCHECK defined
- ✅ No secrets in layers
- ✅ Minimal base image

### 📊 Resumen
- **Críticas:** 1
- **Altas:** 3
- **Medias:** 5
- **Bajas:** 8
```

## Herramientas Utilizadas

| Herramienta | Función | Descripción |
|-------------|---------|-------------|
| Trivy | Vulnerabilidades | Scanner de vulnerabilidades para containers |
| Grype | Vulnerabilidades | Análisis de vulnerabilidades de Anchore |
| Hadolint | Linting | Linter para Dockerfiles |
| Dockle | Best Practices | Verificación de mejores prácticas |
| Syft | SBOM | Generador de Software Bill of Materials |

## Checks de Seguridad

### Dockerfile
- [ ] No usar `latest` tag
- [ ] Pinear versiones de paquetes
- [ ] No ejecutar como root (usar USER)
- [ ] Usar multi-stage builds
- [ ] No copiar secrets
- [ ] Definir HEALTHCHECK
- [ ] Minimizar capas

### Imagen
- [ ] Imagen base actualizada
- [ ] Sin vulnerabilidades críticas
- [ ] Sin secrets expuestos
- [ ] Permisos mínimos
- [ ] Sin paquetes innecesarios

## Security Gates

- ❌ **FAIL** si hay vulnerabilidades críticas en imagen base
- ❌ **FAIL** si se ejecuta como root sin justificación
- ⚠️ **WARN** si hay más de 5 vulnerabilidades altas
- ✅ **PASS** en caso contrario

## Recomendaciones Automáticas

1. **Actualizar imagen base**
   ```dockerfile
   FROM nginx:1.25-alpine  # En lugar de nginx:latest
   ```

2. **No ejecutar como root**
   ```dockerfile
   USER nginx
   ```

3. **Agregar HEALTHCHECK**
   ```dockerfile
   HEALTHCHECK --interval=30s CMD curl -f http://localhost/ || exit 1
   ```
