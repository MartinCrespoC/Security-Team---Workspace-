---
description: Generate and manage security awareness training materials
---

# 📚 Training Generation Workflow

## Overview
This workflow helps create security awareness training modules and materials.

## Steps

### 1. Identify Training Need
Determine the training topic:
- **Phishing**: Email security awareness
- **Social Engineering**: Manipulation defense
- **Password Security**: Credential management
- **Incident Response**: Security incident handling
- **Ransomware**: Malware prevention
- **Remediation**: Post-incident training

### 2. Configure Module
Ask for:
- **Topic**: From available topics
- **Custom Name**: Optional custom module name
- **Difficulty**: basic, intermediate, advanced
- **Include Quiz**: Yes/No

// turbo
### 3. Generate Content
```bash
python3 tools/custom-scripts/training_generator.py generate \
  --topic "{topic}"
```

### 4. Review Generated Content
- Check content accuracy
- Verify quiz questions
- Adjust difficulty if needed

### 5. Deploy Module
- Add to LMS
- Assign to users/departments
- Set completion deadlines

### 6. Track Completion
- Monitor completion rates
- Send reminders
- Generate completion reports

## Available Topics

| Topic | Duration | Difficulty |
|-------|----------|------------|
| phishing | 30 min | Basic |
| social_engineering | 45 min | Intermediate |
| password_security | 20 min | Basic |
| incident_response | 60 min | Advanced |
| ransomware | 35 min | Intermediate |

## Quick Commands

```bash
# List available topics
python3 tools/custom-scripts/training_generator.py list

# Generate module
python3 tools/custom-scripts/training_generator.py generate --topic phishing

# Generate without quiz
python3 tools/custom-scripts/training_generator.py generate --topic phishing --no-quiz
```
