---
description: Ejecutar pipeline completo de seguridad DevSecOps
---

# 🔄 /full-pipeline - Pipeline Completo de Seguridad

Este workflow ejecuta todas las etapas del pipeline de seguridad DevSecOps.

## Pipeline Stages

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ SECRETS │──▶│  SAST   │──▶│   SCA   │──▶│   IaC   │──▶│CONTAINER│──▶│ REPORT  │
│  SCAN   │   │  SCAN   │   │  SCAN   │   │  SCAN   │   │  SCAN   │   │GENERATE │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

## Pasos

### Stage 1: Secret Detection 🔑
1. **Ejecutar Gitleaks**
   ```bash
   gitleaks detect --source . --report-format json --report-path scans/secrets/gitleaks.json
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

### Stage 2: SAST Scan 📊
4. **Ejecutar Semgrep**
   ```bash
   semgrep scan --config auto . --json > scans/sast/semgrep.json
   ```
   // turbo

5. **Ejecutar scanners específicos por lenguaje**
   - Bandit (Python)
   - ESLint Security (JavaScript)
   - Gosec (Go)
   - Brakeman (Ruby)

### Stage 3: SCA Scan 📦
6. **Ejecutar análisis de dependencias**
   ```bash
   snyk test --json > scans/sca/snyk.json
   ```

7. **Ejecutar auditorías específicas**
   - Safety/pip-audit (Python)
   - npm audit (Node.js)
   - bundler-audit (Ruby)

### Stage 4: IaC Security 🏗️
8. **Ejecutar Checkov**
   ```bash
   checkov -d . -o json > scans/iac/checkov.json
   ```
   // turbo

9. **Ejecutar tfsec (si hay Terraform)**
   ```bash
   tfsec . --format json > scans/iac/tfsec.json
   ```

10. **Ejecutar KICS**
    ```bash
    kics scan -p . -o json > scans/iac/kics.json
    ```

### Stage 5: Container Security 🐳
11. **Escanear Dockerfiles**
    ```bash
    hadolint Dockerfile --format json > scans/containers/hadolint.json
    ```
    // turbo

12. **Escanear imágenes (si aplica)**
    ```bash
    trivy image <imagen> --format json > scans/containers/trivy.json
    ```

### Stage 6: Report Generation 📈
13. **Consolidar resultados**
14. **Generar reporte ejecutivo**
15. **Evaluar security gates**
16. **Notificar resultados**

## Uso

```bash
# Pipeline completo
/full-pipeline

# Pipeline con imagen Docker
/full-pipeline --image nginx:latest

# Solo etapas específicas
/full-pipeline --stages secrets sast sca
```

## Uso Alternativo

Ejecutar el script directamente:
```bash
python tools/custom-scripts/pipeline_security.py
python tools/custom-scripts/pipeline_security.py --stages secrets sast
python tools/custom-scripts/pipeline_security.py --image nginx:latest
```

## Output Esperado

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    🔄 Security Pipeline Orchestrator                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════
🔄 Stage 1: Secret Detection
═══════════════════════════════════════════════════════════════════════════
[INFO] Ejecutando Gitleaks...
[✓] Gitleaks: 0 secrets encontrados
[INFO] Ejecutando TruffleHog...
[✓] TruffleHog: 0 credenciales encontradas
✅ Secret Detection: PASSED

═══════════════════════════════════════════════════════════════════════════
🔄 Stage 2: SAST Scan
═══════════════════════════════════════════════════════════════════════════
[INFO] Ejecutando Semgrep...
[✓] Semgrep completado
[INFO] Ejecutando Bandit...
[✓] Bandit completado
⚠️ SAST Scan: WARNING (3 high vulnerabilities)

═══════════════════════════════════════════════════════════════════════════
📊 RESUMEN DEL PIPELINE
═══════════════════════════════════════════════════════════════════════════

Etapa                     Estado          Duración     Findings
──────────────────────────────────────────────────────────────────────────
Secret Detection          ✅ passed        2.34s       -
SAST Scan                 ⚠️ warning       15.67s      high:3, medium:5
SCA Scan                  ✅ passed        8.23s       low:2
IaC Security              ✅ passed        5.12s       -
Container Security        ✅ passed        12.45s      medium:1

──────────────────────────────────────────────────────────────────────────
Duración total: 43.81 segundos
──────────────────────────────────────────────────────────────────────────

⚠️ SECURITY GATE: WARNING

Reportes: scans/pipeline/20240504_194532/
```

## Security Gates

| Criterio | Umbral | Acción |
|----------|--------|--------|
| Vulnerabilidades Críticas | 0 | ❌ FAIL |
| Vulnerabilidades Altas | ≤ 5 | ⚠️ WARN si > 5 |
| Secrets Expuestos | 0 | ❌ FAIL |
| Misconfigurations Críticas | 0 | ❌ FAIL |

## Integración CI/CD

### GitHub Actions
```yaml
- name: Run Security Pipeline
  run: python tools/custom-scripts/pipeline_security.py
  continue-on-error: false
```

### GitLab CI
```yaml
security_pipeline:
  script:
    - python tools/custom-scripts/pipeline_security.py
  allow_failure: false
```

### Jenkins
```groovy
stage('Security Pipeline') {
    steps {
        sh 'python tools/custom-scripts/pipeline_security.py'
    }
}
```

## Reportes Generados

| Archivo | Descripción |
|---------|-------------|
| `pipeline_report.md` | Reporte ejecutivo en Markdown |
| `pipeline_report.json` | Reporte estructurado en JSON |
| `gitleaks.json` | Resultados de Gitleaks |
| `semgrep.json` | Resultados de Semgrep |
| `snyk.json` | Resultados de Snyk |
| `checkov.json` | Resultados de Checkov |
| `trivy.json` | Resultados de Trivy |

## Notificaciones

- 📧 Email al equipo de seguridad si hay vulnerabilidades críticas
- 💬 Slack notification con resumen del pipeline
- 📝 Crear issues automáticamente para vulnerabilidades
