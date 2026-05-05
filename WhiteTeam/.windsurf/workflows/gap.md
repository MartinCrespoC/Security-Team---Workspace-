---
description: Perform gap analysis against compliance frameworks
---

# /gap - Gap Analysis Workflow

## Overview
This workflow performs a comprehensive gap analysis comparing current control implementation against framework requirements.

## Usage
```
/gap [--framework X] [--target N] [--roadmap]
```

## Steps

### 1. Select Framework
Choose the framework for analysis:
- **ISO27001**: ISO 27001:2022
- **SOC2**: SOC 2 Type II
- **PCI-DSS**: PCI-DSS v4.0

### 2. Set Target Compliance
Define target compliance level:
- Default: 100%
- Minimum recommended: 80%
- Certification requirement: Usually 95%+

### 3. Run Gap Analysis
// turbo
```bash
python tools/custom-scripts/gap_analysis.py --framework ISO27001 --target 100
```

### 4. Review Results
The analysis will show:
- Current compliance percentage
- Gap percentage
- Domain-by-domain breakdown
- List of gaps by priority

### 5. Prioritize Gaps
Gaps are prioritized by:
- **Critical**: Immediate action required
- **High**: Address within 30 days
- **Medium**: Address within 60 days
- **Low**: Address within 90 days

### 6. Review Remediation Roadmap
The tool generates a phased roadmap:
- Phase 1: Critical and high priority gaps
- Phase 2: Medium priority gaps
- Phase 3: Low priority gaps

### 7. Estimate Resources
For each gap:
- Effort hours required
- Skills needed
- Dependencies
- Budget implications

### 8. Create Action Plan
For each gap:
- Define specific remediation steps
- Assign owner
- Set due date
- Define success criteria
- Identify dependencies

### 9. Track Progress
- Update control status as remediation completes
- Re-run gap analysis periodically
- Report progress to stakeholders

## Gap Analysis Output

```yaml
framework: ISO27001
current_compliance: 72.5%
target_compliance: 100%
gap_percentage: 27.5%
total_gaps: 25
critical_gaps: 3
estimated_effort_hours: 480

domains:
  - domain: A.5 Organizational Controls
    compliance: 80%
    gaps: 8
  - domain: A.8 Technological Controls
    compliance: 65%
    gaps: 12

remediation_roadmap:
  - phase: 1
    estimated_hours: 160
    items:
      - control: A.8.2 Privileged Access
        priority: critical
        effort: 40h
```

## Priority Matrix

| Priority | SLA | Risk Level | Action |
|----------|-----|------------|--------|
| Critical | 7 days | Very High | Immediate |
| High | 30 days | High | Urgent |
| Medium | 60 days | Medium | Planned |
| Low | 90 days | Low | Scheduled |

## Output Files
- `reports/compliance/gap_analysis_[FRAMEWORK]_[DATE].yaml`
- `reports/compliance/gap_analysis_[FRAMEWORK]_[DATE].json`

## Quick Commands

Full gap analysis:
```bash
python tools/custom-scripts/gap_analysis.py --framework ISO27001 --target 100
```

With JSON output:
```bash
python tools/custom-scripts/gap_analysis.py --framework SOC2 --format json
```

## Related Workflows
- `/compliance` - Quick compliance check
- `/audit` - Full compliance audit
- `/control` - Control implementation
- `/risk` - Risk assessment for gaps
