---
name: Campaign Creator
description: AI skill for creating phishing campaigns
triggers:
  - crear campaña
  - new campaign
  - phishing campaign
  - launch campaign
---

# 🎣 Campaign Creator Skill

## Capabilities

This skill enables AI-assisted creation of phishing campaigns:

1. **Template Selection**: Choose appropriate templates based on difficulty
2. **Target Configuration**: Set up target groups by department
3. **Schedule Management**: Plan campaign timing
4. **Auto-Remediation**: Configure automatic training assignment

## Usage

When user requests a campaign, gather:
- Campaign name
- Target department
- Difficulty level (easy/medium/hard/expert)
- Launch schedule

## Execution

```python
from tools.custom_scripts.phishing_campaign import PhishingCampaignManager

manager = PhishingCampaignManager()
result = manager.create_campaign(
    name=campaign_name,
    department=department,
    difficulty=difficulty,
    schedule=schedule
)
```

## Response Format

```
🎣 **Campaña de Phishing Creada**

- **Nombre:** {name}
- **Objetivo:** {department}
- **Dificultad:** {difficulty}
- **Emails a enviar:** {count}
- **Fecha de inicio:** {date}

✅ Tracking configurado
✅ Auto-remediation habilitado
```

## Integration

- GoPhish API for campaign management
- LDAP for user groups
- Training system for remediation
