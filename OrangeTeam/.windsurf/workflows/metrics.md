---
description: View and analyze security awareness metrics and KPIs
---

# 📊 Metrics Analysis Workflow

## Overview
This workflow provides access to security awareness metrics, dashboards, and reports.

## Steps

### 1. Collect Current Metrics
Gather data from all sources:
- Phishing campaign results
- Training completion rates
- Quiz scores
- User risk scores

// turbo
### 2. Display Dashboard
```bash
python3 tools/custom-scripts/awareness_metrics.py dashboard
```

### 3. Analyze Trends
Review key metrics:
- **Click Rate**: Target <5%
- **Report Rate**: Target >80%
- **Training Completion**: Target >95%
- **Security Score**: Target >85

### 4. Identify Issues
- High-risk users
- Underperforming departments
- Training gaps
- Repeat offenders

### 5. Generate Reports
```bash
# Console report
python3 tools/custom-scripts/awareness_metrics.py report

# JSON export
python3 tools/custom-scripts/awareness_metrics.py report --format json --output report.json

# Markdown report
python3 tools/custom-scripts/awareness_metrics.py report --format markdown --output report.md
```

### 6. Take Action
Based on metrics:
- Assign additional training
- Launch targeted campaigns
- Escalate high-risk users
- Adjust awareness programs

## Key Performance Indicators

| KPI | Target | Warning | Critical |
|-----|--------|---------|----------|
| Click Rate | <5% | >10% | >15% |
| Report Rate | >80% | <60% | <40% |
| Training Completion | >95% | <85% | <75% |
| Credential Submit | <2% | >5% | >10% |
| Time to Report | <5 min | >15 min | >30 min |

## Quick Commands

```bash
# Show dashboard
python3 tools/custom-scripts/awareness_metrics.py dashboard

# Collect metrics
python3 tools/custom-scripts/awareness_metrics.py collect

# Calculate user risk
python3 tools/custom-scripts/awareness_metrics.py risk --email user@company.com
```
