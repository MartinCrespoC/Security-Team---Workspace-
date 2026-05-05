---
name: Purple Team Integrator
description: AI skill for Purple Team integration and collaboration
triggers:
  - purple team
  - integrate red team
  - share with blue
  - team collaboration
---

# 💜 Purple Team Integrator Skill

## Overview

This skill manages integration between Orange Team and other Purple Team components.

## Team Integration Matrix

### 🔴 Red Team Integration
**Receive from Red Team:**
- New attack vectors discovered in pentests
- Social engineering techniques
- Phishing templates based on real attacks

**Send to Red Team:**
- User susceptibility data
- High-value targets
- Successful phishing patterns

### 🔵 Blue Team Integration
**Receive from Blue Team:**
- Incident reports involving phishing
- Detection rule effectiveness
- User behavior anomalies

**Send to Blue Team:**
- Phishing indicators
- User behavior baselines
- Training completion data

### 🟡 Yellow Team (DevSecOps)
**Receive:**
- Secure coding guidelines
- Application security training needs

**Send:**
- Developer security awareness metrics
- Code review training completion

### 🟢 Green Team (SIEM/SOC)
**Receive:**
- Alert patterns
- Incident timelines

**Send:**
- User risk scores
- Anomaly patterns
- Phishing report events

### ⚪ White Team (Compliance)
**Receive:**
- Compliance requirements
- Audit findings

**Send:**
- Awareness metrics
- Training compliance reports
- Risk assessments

## API Integration

```python
class PurpleTeamIntegration:
    def share_with_red_team(self, data):
        # Share susceptibility data
        pass
    
    def receive_from_red_team(self, attack_vector):
        # Create awareness campaign
        pass
    
    def share_with_blue_team(self, data):
        # Share behavior patterns
        pass
    
    def receive_from_blue_team(self, incident):
        # Create training from incident
        pass
```

## Data Exchange Format

```json
{
  "source": "orange_team",
  "destination": "red_team",
  "data_type": "susceptibility_report",
  "timestamp": "2024-01-15T10:30:00Z",
  "payload": {
    "high_risk_departments": ["sales", "marketing"],
    "click_rate_by_dept": {...},
    "successful_techniques": [...]
  }
}
```

## Collaboration Workflows

1. **Attack Vector → Training**: Red Team finds vector → Orange creates training
2. **Incident → Awareness**: Blue detects incident → Orange runs campaign
3. **Metrics → Detection**: Orange provides baselines → Green improves detection
4. **Compliance → Training**: White requires training → Orange delivers
