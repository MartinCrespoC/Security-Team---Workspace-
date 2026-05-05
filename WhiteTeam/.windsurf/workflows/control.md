---
description: Map and manage security controls across frameworks
---

# /control - Control Mapping Workflow

## Overview
This workflow helps map security controls across multiple compliance frameworks and manage their implementation status.

## Usage
```
/control [id] [--map-to frameworks] [--status] [--create]
```

## Steps

### 1. Identify Control
Specify the control to work with:
- By ID: `A.5.1`, `CC6.1`, `8.3`
- By name: "Access Control", "MFA"
- New control: `--create`

### 2. Control Information
Gather control details:
- **ID**: Unique identifier
- **Name**: Descriptive name
- **Description**: What the control does
- **Category**: Technical, Administrative, Physical
- **Owner**: Responsible person

### 3. Framework Mapping
Map control to applicable frameworks:

| Framework | Reference Format |
|-----------|-----------------|
| ISO 27001 | A.X.X |
| SOC 2 | CCX.X, AX.X |
| PCI-DSS | X.X.X |
| GDPR | Art. X |
| HIPAA | §164.XXX |
| NIST CSF | XX.XX-X |

### 4. Create Control Record
```yaml
control:
  id: CTRL-001
  name: Multi-Factor Authentication
  description: Require MFA for all remote access
  category: Technical
  frameworks:
    ISO27001: A.8.5
    SOC2: CC6.1
    PCI-DSS: 8.4
    NIST_CSF: PR.AC-7
  implementation_status: implemented
  owner: IT Security
  evidence:
    - MFA configuration screenshots
    - User enrollment reports
  last_review: 2024-01-15
  next_review: 2024-07-15
```

### 5. Implementation Status
Track implementation:
- **Implemented**: Fully operational
- **Partial**: Partially implemented
- **Planned**: In roadmap
- **Not Implemented**: Gap exists
- **Not Applicable**: Doesn't apply

### 6. Evidence Collection
Link evidence to control:
- Screenshots
- Configuration files
- Logs
- Policies
- Procedures

### 7. Save Control
Save to controls directory:
```
controls/
├── technical/
│   └── CTRL-001.yaml
├── administrative/
│   └── CTRL-002.yaml
├── physical/
│   └── CTRL-003.yaml
└── mappings/
    └── framework_mappings.yaml
```

### 8. Cross-Reference
View control across frameworks:
```
Control: Multi-Factor Authentication (CTRL-001)

ISO 27001:  A.8.5 - Secure authentication
SOC 2:      CC6.1 - Logical access security
PCI-DSS:    8.4   - MFA for CDE access
NIST CSF:   PR.AC-7 - Authentication
HIPAA:      §164.312(d) - Authentication
```

## Control Categories

### Technical Controls
- Access control systems
- Encryption
- Firewalls
- Intrusion detection
- Antivirus
- MFA

### Administrative Controls
- Policies
- Procedures
- Training
- Background checks
- Risk assessments

### Physical Controls
- Locks
- Cameras
- Guards
- Environmental controls
- Badge access

## Common Control Mappings

| Control | ISO 27001 | SOC 2 | PCI-DSS | NIST CSF |
|---------|-----------|-------|---------|----------|
| MFA | A.8.5 | CC6.1 | 8.4 | PR.AC-7 |
| Access Review | A.5.18 | CC6.4 | 7.2 | PR.AC-4 |
| Encryption | A.8.24 | CC6.7 | 3.4 | PR.DS-1 |
| Logging | A.8.15 | CC7.2 | 10.1 | DE.CM-1 |
| Incident Response | A.5.24 | CC7.4 | 12.10 | RS.RP-1 |
| Backup | A.8.13 | A1.2 | 9.5 | PR.IP-4 |

## Output Files
- `controls/[category]/CTRL-XXX.yaml`
- `controls/mappings/framework_mappings.yaml`

## Related Workflows
- `/compliance` - Verify control compliance
- `/audit` - Audit control effectiveness
- `/evidence` - Collect control evidence
- `/gap` - Identify control gaps
