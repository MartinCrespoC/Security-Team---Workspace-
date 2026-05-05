---
name: Report Generator
description: AI skill for generating security awareness reports
triggers:
  - generar reporte
  - generate report
  - executive summary
  - compliance report
---

# 📄 Report Generator Skill

## Capabilities

This skill generates various security awareness reports:

1. **Executive Reports**: High-level summaries for leadership
2. **Compliance Reports**: Audit-ready documentation
3. **Campaign Reports**: Detailed phishing campaign results
4. **Training Reports**: Completion and effectiveness metrics

## Report Types

### Executive Summary
- KPI overview
- Trend analysis
- Risk highlights
- Recommendations

### Compliance Report
- Training completion rates
- Policy acknowledgments
- Audit trail
- Remediation status

### Campaign Report
- Campaign statistics
- User behavior analysis
- Department comparison
- Improvement trends

### Training Report
- Module completion
- Quiz scores
- Learning paths
- Certification status

## Usage

```python
from tools.custom_scripts.awareness_metrics import AwarenessMetricsAnalyzer

analyzer = AwarenessMetricsAnalyzer()

# Console report
analyzer.generate_report(format="console")

# JSON export
analyzer.generate_report(format="json", output="report.json")

# Markdown report
analyzer.generate_report(format="markdown", output="report.md")
```

## Output Formats

| Format | Use Case |
|--------|----------|
| Console | Quick review |
| JSON | API integration |
| Markdown | Documentation |
| PDF | Executive distribution |

## Report Sections

```markdown
# Security Awareness Report

## Executive Summary
- Overall security score
- Key metrics
- Critical findings

## Metrics Detail
- Click rates by department
- Training completion
- Risk scores

## Trends
- Month-over-month comparison
- Year-over-year progress

## Recommendations
- Priority actions
- Resource needs
- Timeline
```
