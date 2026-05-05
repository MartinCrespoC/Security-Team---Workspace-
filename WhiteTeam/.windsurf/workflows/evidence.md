---
description: Collect and manage compliance evidence
---

# /evidence - Evidence Collection Workflow

## Overview
This workflow guides the collection, organization, and management of compliance evidence for audits and assessments.

## Usage
```
/evidence [--control X] [--period Y] [--type screenshot|log|config|document]
```

## Steps

### 1. Identify Evidence Requirements
Determine what evidence is needed:
- Control being evidenced
- Framework requirement
- Evidence type
- Time period

### 2. Evidence Types

| Type | Description | Examples |
|------|-------------|----------|
| Screenshot | Visual proof | Config screens, dashboards |
| Log | System logs | Access logs, audit trails |
| Config | Configuration files | Firewall rules, policies |
| Document | Written documentation | Policies, procedures |
| Report | Generated reports | Scan results, assessments |
| Interview | Verbal confirmation | Meeting notes, recordings |

### 3. Collection Guidelines

**Screenshots:**
- Include timestamp
- Show full context
- Highlight relevant areas
- Include system identification

**Logs:**
- Define time range
- Include relevant entries only
- Preserve original format
- Document source system

**Configurations:**
- Export current config
- Remove sensitive data
- Document version/date
- Include system info

**Documents:**
- Current version only
- Include approval signatures
- Show effective date
- Document location

### 4. Naming Convention
```
EVD-[CONTROL]-[DATE]-[DESCRIPTION].[ext]

Examples:
- EVD-A.8.5-20240115-MFA_Config.png
- EVD-CC6.1-20240115-Access_Logs.csv
- EVD-8.4-20240115-MFA_Policy.pdf
```

### 5. Metadata Requirements
Each evidence item should include:
```yaml
evidence:
  id: EVD-001
  control_id: A.8.5
  type: screenshot
  description: MFA configuration in Azure AD
  collected_by: John Smith
  collected_date: 2024-01-15
  period_start: 2024-01-01
  period_end: 2024-01-15
  source_system: Azure Active Directory
  file_path: evidence/screenshots/EVD-A.8.5-20240115-MFA_Config.png
  hash: sha256:abc123...
```

### 6. Storage Organization
```
evidence/
├── screenshots/
│   ├── 2024-Q1/
│   │   ├── EVD-A.8.5-20240115-MFA_Config.png
│   │   └── EVD-CC6.1-20240115-Access_Review.png
│   └── 2024-Q2/
├── logs/
│   ├── access/
│   ├── audit/
│   └── security/
├── configs/
│   ├── network/
│   ├── systems/
│   └── applications/
├── documents/
│   ├── policies/
│   ├── procedures/
│   └── reports/
└── register.yaml
```

### 7. Evidence Register
Maintain a register of all evidence:
```yaml
evidence_register:
  last_updated: 2024-01-15
  items:
    - id: EVD-001
      control: A.8.5
      type: screenshot
      path: screenshots/2024-Q1/EVD-A.8.5-20240115-MFA_Config.png
      status: current
    - id: EVD-002
      control: CC6.1
      type: log
      path: logs/access/EVD-CC6.1-20240115-Access_Logs.csv
      status: current
```

### 8. Validation
Verify evidence:
- [ ] Relevant to control
- [ ] Within required time period
- [ ] Complete and readable
- [ ] Properly labeled
- [ ] Metadata recorded

### 9. Retention
Evidence retention periods:
- Audit evidence: 7 years
- Compliance evidence: 5 years
- Operational evidence: 3 years

## Evidence by Framework

### ISO 27001
- Policy documents
- Risk assessments
- Training records
- Access reviews
- Incident reports

### SOC 2
- Control descriptions
- Testing results
- Exception reports
- Change records
- Monitoring logs

### PCI-DSS
- Network diagrams
- Scan reports
- Penetration tests
- Access logs
- Configuration standards

### GDPR
- Privacy notices
- Consent records
- DPIA documents
- Data inventories
- Breach notifications

### HIPAA
- Risk analyses
- BAA agreements
- Training records
- Access logs
- Incident documentation

## Output Files
- `evidence/[type]/[period]/EVD-XXX.[ext]`
- `evidence/register.yaml`

## Related Workflows
- `/audit` - Use evidence in audits
- `/compliance` - Verify evidence coverage
- `/control` - Link evidence to controls
