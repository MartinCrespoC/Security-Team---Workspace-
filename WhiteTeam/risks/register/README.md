# Risk Register

This directory contains the organization's risk register.

## Structure

Each risk is stored as a YAML file with the naming convention:
```
RISK-[YEAR]-[ID].yaml
```

## Risk Template

```yaml
risk:
  id: RISK-2024-001
  title: "Risk Title"
  description: "Detailed description"
  category: operational  # strategic, operational, financial, compliance, technology, third_party
  asset: "Affected asset"
  threat: "Threat description"
  vulnerability: "Vulnerability description"
  
  inherent_risk:
    likelihood: 3  # 1-5
    impact: 4      # 1-5
    score: 12      # likelihood × impact
    level: medium  # critical, high, medium, low, very_low
  
  controls:
    - id: CTRL-001
      name: "Control name"
      effectiveness: 70  # 0-100%
  
  residual_risk:
    likelihood: 2
    impact: 3
    score: 6
    level: low
  
  treatment:
    strategy: mitigate  # mitigate, transfer, accept, avoid
    actions:
      - "Action 1"
      - "Action 2"
    owner: "Risk Owner"
    due_date: "2024-12-31"
    status: in_progress
  
  status: open  # open, in_progress, closed, accepted
  created_date: "2024-01-15"
  last_updated: "2024-01-15"
  owner: "Risk Owner"
  notes: "Additional notes"
```

## Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 20-25 | Critical | Immediate action |
| 15-19 | High | Priority remediation |
| 8-14 | Medium | Planned mitigation |
| 4-7 | Low | Monitor |
| 1-3 | Very Low | Accept |
