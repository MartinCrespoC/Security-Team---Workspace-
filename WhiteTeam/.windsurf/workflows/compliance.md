---
description: Verify compliance status against security frameworks
---

# /compliance - Compliance Verification Workflow

## Overview
This workflow checks the current compliance status against one or more security frameworks and generates a compliance report.

## Usage
```
/compliance [--framework X] [--check all] [--report pdf|html|md]
```

## Steps

### 1. Select Framework(s)
Choose which framework(s) to check:
- **ISO27001**: ISO 27001:2022 ISMS
- **SOC2**: SOC 2 Type II Trust Services
- **PCI-DSS**: PCI-DSS v4.0
- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability
- **NIST-CSF**: NIST Cybersecurity Framework 2.0
- **all**: Check all frameworks

### 2. Run Compliance Check
// turbo
```bash
python tools/custom-scripts/compliance_check.py --framework all --format console
```

### 3. Review Results
The compliance check will show:
- Overall compliance score per framework
- Control status breakdown:
  - ✅ Compliant
  - ⚠️ Partial
  - ❌ Non-Compliant
  - ➖ Not Applicable
  - 🔵 Not Assessed
- List of findings

### 4. Analyze Gaps
For non-compliant controls:
// turbo
```bash
python tools/custom-scripts/gap_analysis.py --framework [FRAMEWORK] --target 100
```

### 5. Generate Detailed Report
// turbo
```bash
python tools/custom-scripts/compliance_check.py --framework [FRAMEWORK] --format markdown
```

### 6. Identify Remediation Actions
For each gap identified:
- Determine root cause
- Define remediation steps
- Assign owner
- Set timeline
- Estimate effort

### 7. Update Control Status
After remediation:
- Update control implementation status
- Collect new evidence
- Re-run compliance check

### 8. Document and Report
- Save compliance report
- Update compliance dashboard
- Notify stakeholders

## Compliance Scoring

**Score Calculation:**
```
Score = (Compliant + Partial×0.5) / (Total - N/A) × 100
```

**Compliance Levels:**
- 🟢 90-100%: Excellent
- 🟡 70-89%: Good (needs improvement)
- 🟠 50-69%: Fair (significant gaps)
- 🔴 <50%: Poor (critical attention needed)

## Output Files
- `reports/compliance/compliance_report_[DATE].md`
- `reports/compliance/compliance_report_[DATE].json`
- `reports/compliance/compliance_report_[DATE].yaml`

## Quick Commands

Check all frameworks:
```bash
python tools/custom-scripts/compliance_check.py --framework all
```

Check specific framework:
```bash
python tools/custom-scripts/compliance_check.py --framework ISO27001
```

Generate JSON report:
```bash
python tools/custom-scripts/compliance_check.py --framework all --format json
```

## Related Workflows
- `/audit` - Full compliance audit
- `/gap` - Detailed gap analysis
- `/control` - Control mapping
- `/evidence` - Evidence collection
