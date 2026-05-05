---
description: Generate GRC reports and dashboards
---

# /report - Report Generation Workflow

## Overview
This workflow generates various GRC reports including executive summaries, compliance status, risk reports, and audit findings.

## Usage
```
/report [type] [--format pdf|html|md] [--period monthly|quarterly|annual]
```

## Report Types

### Executive Summary
High-level overview for leadership:
- Overall compliance score
- Key risks
- Critical findings
- Trends and progress

### Compliance Status
Detailed compliance report:
- Framework-by-framework status
- Control implementation
- Gap analysis
- Remediation progress

### Risk Report
Risk management report:
- Risk register summary
- New risks identified
- Treatment progress
- Risk trends

### Audit Report
Audit findings report:
- Audit scope and objectives
- Findings by severity
- Remediation status
- Follow-up items

### KPI Dashboard
Key performance indicators:
- Compliance metrics
- Risk metrics
- Audit metrics
- Trend analysis

## Steps

### 1. Select Report Type
Choose the report to generate:
- `executive` - Executive summary
- `compliance` - Compliance status
- `risk` - Risk report
- `audit` - Audit findings
- `kpi` - KPI dashboard

### 2. Define Parameters
Specify report parameters:
- Time period
- Frameworks to include
- Level of detail
- Recipients

### 3. Gather Data
Collect data from:
- `controls/` - Control status
- `risks/` - Risk register
- `audits/` - Audit findings
- `compliance/` - Evidence

### 4. Generate Report
// turbo
```bash
python tools/custom-scripts/compliance_check.py --framework all --format markdown
```

### 5. Review and Edit
- Verify data accuracy
- Add commentary
- Include recommendations
- Format for audience

### 6. Export
Export in desired format:
- PDF for distribution
- HTML for web viewing
- Markdown for documentation

### 7. Distribute
- Email to stakeholders
- Upload to GRC platform
- Present to leadership

## Report Templates

### Executive Summary Template
```markdown
# GRC Executive Summary - [Period]

## Overall Status
- Compliance Score: XX%
- Open Risks: XX (X Critical)
- Open Findings: XX

## Key Highlights
- [Highlight 1]
- [Highlight 2]

## Areas of Concern
- [Concern 1]
- [Concern 2]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]

## Next Steps
- [Action 1]
- [Action 2]
```

### KPI Dashboard Metrics

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Overall Compliance | ≥90% | XX% | ↑↓→ |
| Critical Risks | 0 | X | ↑↓→ |
| Open Findings | ≤10 | X | ↑↓→ |
| Remediation Rate | ≥95% | XX% | ↑↓→ |
| Training Completion | 100% | XX% | ↑↓→ |

## Report Schedule

| Report | Frequency | Audience | Due |
|--------|-----------|----------|-----|
| Executive Summary | Monthly | C-Suite | 5th |
| Compliance Status | Quarterly | Management | 15th |
| Risk Report | Monthly | Risk Committee | 10th |
| Audit Report | Per Audit | Audit Committee | +30 days |
| KPI Dashboard | Weekly | Security Team | Monday |

## Output Files
- `reports/executive/[DATE]_executive_summary.md`
- `reports/compliance/[DATE]_compliance_report.md`
- `reports/technical/[DATE]_risk_report.md`

## Quick Commands

Generate compliance report:
```bash
python tools/custom-scripts/compliance_check.py --framework all --format markdown
```

Generate risk summary:
```bash
python tools/custom-scripts/risk_assessment.py --list
```

Generate gap analysis:
```bash
python tools/custom-scripts/gap_analysis.py --framework ISO27001
```

## Related Workflows
- `/compliance` - Compliance verification
- `/risk` - Risk assessment
- `/audit` - Audit execution
- `/gap` - Gap analysis
