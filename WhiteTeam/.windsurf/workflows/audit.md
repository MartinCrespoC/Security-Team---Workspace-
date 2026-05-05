---
description: Execute a compliance audit for a specific framework
---

# /audit - Compliance Audit Workflow

## Overview
This workflow guides you through executing a compliance audit against security frameworks like ISO 27001, SOC 2, PCI-DSS, GDPR, or HIPAA.

## Usage
```
/audit [framework] [--scope "scope"] [--type internal|external]
```

## Steps

### 1. Determine Audit Parameters
Ask the user for:
- **Framework**: ISO27001, SOC2, PCI-DSS, GDPR, HIPAA, NIST-CSF
- **Scope**: Full audit or specific domain (e.g., "Access Control", "A.8")
- **Type**: Internal, External, Compliance, Follow-up

### 2. Generate Audit Checklist
// turbo
```bash
python tools/custom-scripts/audit_checklist.py --framework [FRAMEWORK] --scope "[SCOPE]" --format markdown
```

### 3. Review Generated Checklist
- Open the generated checklist from `audits/checklists/`
- Review controls to be tested
- Identify evidence requirements

### 4. Create Audit Plan
Generate an audit plan including:
- Timeline (start/end dates)
- Resource allocation
- Interview schedule
- Evidence collection plan

### 5. Execute Testing
For each control in the checklist:
1. Collect required evidence
2. Perform testing procedures
3. Document findings
4. Assign status (Pass/Fail/Partial/N/A)

### 6. Document Findings
For any non-compliant controls:
- Create finding record with severity
- Document root cause
- Propose remediation
- Assign owner and due date

### 7. Generate Audit Report
// turbo
```bash
python tools/custom-scripts/compliance_check.py --framework [FRAMEWORK] --format markdown
```

### 8. Review and Finalize
- Review findings with stakeholders
- Obtain management response
- Finalize audit report
- Schedule follow-up

## Output Files
- `audits/checklists/AUD-[ID].yaml` - Audit checklist
- `audits/reports/AUD-[ID]-report.md` - Audit report
- `audits/internal/[YEAR]/` - Audit documentation

## Related Workflows
- `/compliance` - Quick compliance check
- `/gap` - Gap analysis
- `/evidence` - Evidence collection
