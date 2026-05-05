---
description: Escanear Infrastructure as Code por misconfigurations
---

# 🏗️ /scan-iac - Escaneo de Infrastructure as Code

Este workflow analiza archivos de IaC (Terraform, Kubernetes, CloudFormation, etc.) por misconfigurations de seguridad.

## Pasos

1. **Detectar tipos de IaC**
   - Terraform (.tf, .tfvars)
   - Kubernetes (.yaml, .yml)
   - CloudFormation (.json, .yaml)
   - Ansible (playbooks)
   - Helm charts

2. **Ejecutar Checkov**
   ```bash
   checkov -d . -o json > scans/iac/checkov.json
   ```
   // turbo

3. **Ejecutar tfsec (Terraform)**
   ```bash
   tfsec . --format json > scans/iac/tfsec.json
   ```
   // turbo

4. **Ejecutar KICS**
   ```bash
   kics scan -p . -o json > scans/iac/kics.json
   ```

5. **Ejecutar Terrascan**
   ```bash
   terrascan scan -d . -o json > scans/iac/terrascan.json
   ```

6. **Generar reporte de compliance**

## Checks de Seguridad

### Terraform
- [ ] No hardcodear secrets
- [ ] Encriptar recursos de almacenamiento
- [ ] Habilitar logging
- [ ] Restringir security groups
- [ ] Usar IAM roles mínimos

### Kubernetes
- [ ] No ejecutar como root
- [ ] Definir resource limits
- [ ] No usar hostNetwork
- [ ] Configurar network policies
- [ ] Usar secrets para credenciales

### CloudFormation
- [ ] Encriptar S3 buckets
- [ ] Habilitar CloudTrail
- [ ] Restringir IAM policies
- [ ] Usar VPC endpoints

## Compliance Frameworks

- CIS Benchmarks
- NIST 800-53
- SOC 2
- PCI DSS
- HIPAA

## Security Gate

- ❌ **FAIL** si hay misconfigurations críticas
- ⚠️ **WARN** si hay misconfigurations altas
- ✅ **PASS** en caso contrario
