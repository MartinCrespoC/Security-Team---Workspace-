---
description: Create and manage phishing campaigns for security awareness testing
---

# 🎣 Phishing Campaign Workflow

## Overview
This workflow guides you through creating, launching, and managing phishing campaigns.

## Steps

### 1. Define Campaign Parameters
Ask the user for:
- **Campaign Name**: Descriptive name for the campaign
- **Target Department**: Which department(s) to target
- **Difficulty Level**: easy, medium, hard, or expert
- **Schedule**: When to launch (immediate or scheduled)

### 2. Select Template
Based on difficulty, recommend appropriate templates:
- **Easy**: Obvious phishing indicators for baseline testing
- **Medium**: Standard credential phishing
- **Hard**: Spear phishing with personalization
- **Expert**: Whaling/BEC simulation

// turbo
### 3. Configure Campaign
```bash
python3 tools/custom-scripts/phishing_campaign.py create \
  --name "{campaign_name}" \
  --department "{department}" \
  --difficulty "{difficulty}"
```

### 4. Review and Launch
- Confirm campaign settings with user
- Launch campaign via GoPhish API
- Set up tracking and auto-remediation

### 5. Monitor Results
```bash
python3 tools/custom-scripts/phishing_campaign.py results --id {campaign_id}
```

### 6. Post-Campaign Actions
- Generate metrics report
- Identify high-risk users
- Assign remediation training
- Schedule follow-up campaign

## Quick Commands

| Command | Description |
|---------|-------------|
| `create` | Create new campaign |
| `list` | List all campaigns |
| `results --id X` | Get campaign results |
| `--remediate` | Auto-assign training |

## Integration Points

- **GoPhish API**: Campaign management
- **Training System**: Auto-assign modules
- **Metrics Dashboard**: Real-time tracking
- **SIEM**: Event logging
