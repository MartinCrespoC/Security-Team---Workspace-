---
description: Generate security policies based on templates and frameworks
---

# /policy - Policy Generation Workflow

## Overview
This workflow generates security policies based on templates, mapped to compliance frameworks.

## Usage
```
/policy [type] [--based-on "reference"] [--interactive]
```

## Available Policy Types

| Type | Name | Code |
|------|------|------|
| `information_security` | Information Security Policy | SEC |
| `access_control` | Access Control Policy | ACC |
| `data_classification` | Data Classification Policy | CLS |
| `acceptable_use` | Acceptable Use Policy | AUP |
| `incident_response` | Incident Response Policy | INC |
| `business_continuity` | Business Continuity Policy | BCP |
| `data_privacy` | Data Privacy Policy | PRV |
| `vendor_management` | Vendor Management Policy | VND |
| `change_management` | Change Management Policy | CHG |
| `secure_development` | Secure Development Policy | DEV |
| `remote_work` | Remote Work Policy | RMT |
| `password` | Password Policy | PWD |

## Steps

### 1. Select Policy Type
List available policy types:
// turbo
```bash
python tools/custom-scripts/policy_generator.py --list
```

### 2. Gather Policy Information
Collect required information:
- **Organization Name**: Your organization
- **Policy Owner**: Usually CISO or Security Manager
- **Approver**: Executive sponsor
- **Classification**: Public, Internal, Confidential, Restricted
- **Version**: Starting version (e.g., 1.0)

### 3. Generate Policy
// turbo
```bash
python tools/custom-scripts/policy_generator.py --type [TYPE] --interactive
```

### 4. Review Generated Policy
The policy will include:
- Purpose and scope
- Definitions
- Policy statements
- Roles and responsibilities
- Compliance requirements
- Framework mappings
- Revision history

### 5. Customize Content
Edit the generated policy to:
- Add organization-specific requirements
- Adjust policy statements
- Update roles and responsibilities
- Add related documents

### 6. Framework Mapping
Verify framework mappings:
- ISO 27001 controls
- SOC 2 criteria
- PCI-DSS requirements
- GDPR articles
- HIPAA sections

### 7. Review and Approval
- Submit for legal review
- Obtain management approval
- Document approval signatures

### 8. Publish and Communicate
- Save to `policies/` directory
- Update policy register
- Communicate to stakeholders
- Schedule awareness training

## Policy Structure

```markdown
# Policy Name

**Código:** POL-XXX-001
**Versión:** 1.0
**Fecha de Vigencia:** YYYY-MM-DD

## 1. Propósito
## 2. Alcance
## 3. Definiciones
## 4. Declaraciones de Política
## 5. Roles y Responsabilidades
## 6. Cumplimiento
## 7. Documentos Relacionados
## 8. Mapeo a Frameworks
## 9. Historial de Revisiones
```

## Naming Convention
```
POL-[CATEGORY]-[NUMBER]-v[VERSION].md

Examples:
- POL-ACC-001-v1.0.md (Access Control Policy v1.0)
- POL-SEC-001-v2.0.md (Security Policy v2.0)
```

## Output Files
- `policies/security/POL-XXX-001-v1.0.md`
- `policies/privacy/POL-PRV-001-v1.0.md`
- `policies/access/POL-ACC-001-v1.0.md`

## Quick Commands

List policy types:
```bash
python tools/custom-scripts/policy_generator.py --list
```

Generate access control policy:
```bash
python tools/custom-scripts/policy_generator.py --type access_control
```

Generate non-interactively:
```bash
python tools/custom-scripts/policy_generator.py --type password --no-interactive
```

## Related Workflows
- `/compliance` - Verify policy compliance
- `/audit` - Audit policy implementation
- `/control` - Map policy to controls
