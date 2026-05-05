---
name: Metrics Analyzer
description: AI skill for analyzing security awareness metrics
triggers:
  - ver métricas
  - show metrics
  - analytics
  - dashboard
  - report
---

# 📊 Metrics Analyzer Skill

## Capabilities

This skill provides intelligent metrics analysis:

1. **KPI Tracking**: Monitor key performance indicators
2. **Trend Analysis**: Identify patterns over time
3. **Risk Assessment**: Calculate user and department risk scores
4. **Recommendations**: Generate actionable insights

## Key Metrics

| Metric | Target | Formula |
|--------|--------|---------|
| Click Rate | <5% | Clicks / Sent × 100 |
| Report Rate | >80% | Reports / Sent × 100 |
| Training Completion | >95% | Completed / Assigned × 100 |
| Security Score | >85 | Weighted average |

## Usage

```python
from tools.custom_scripts.awareness_metrics import AwarenessMetricsAnalyzer

analyzer = AwarenessMetricsAnalyzer()
analyzer.generate_dashboard()
```

## Response Format

```
📊 **Reporte de Métricas**

**KPIs Principales:**
- Click Rate: {click_rate}% (objetivo: <5%)
- Report Rate: {report_rate}% (objetivo: >80%)
- Training Completion: {completion}%
- Security Score: {score}/100

**Tendencias:**
- {trend_summary}

**Recomendaciones:**
- {recommendations}
```

## Analysis Features

- Department comparison
- Time-based trends
- High-risk user identification
- Predictive risk scoring
