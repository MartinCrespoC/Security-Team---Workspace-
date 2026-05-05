---
description: Assess and manage security risks
---

# /risk - Risk Assessment Workflow

## Overview
This workflow guides you through identifying, assessing, and treating security risks using a quantitative methodology.

## Usage
```
/risk [asset] [--threat "threat"] [--new] [--list]
```

## Steps

### 1. Risk Identification
Gather information about the risk:
- **Asset**: What asset is at risk?
- **Threat**: What is the threat?
- **Vulnerability**: What vulnerability could be exploited?
- **Category**: Strategic, Operational, Financial, Compliance, Technology, Third-Party

### 2. Inherent Risk Assessment
Calculate inherent risk (before controls):

**Likelihood Scale (1-5):**
- 1: Very Low (<10% probability)
- 2: Low (10-30% probability)
- 3: Medium (30-60% probability)
- 4: High (60-90% probability)
- 5: Very High (>90% probability)

**Impact Scale (1-5):**
- 1: Very Low - Insignificant impact
- 2: Low - Minor impact, easy recovery
- 3: Medium - Moderate impact, requires effort
- 4: High - Significant impact, considerable damage
- 5: Very High - Catastrophic impact, severe damage

**Inherent Risk Score = Likelihood × Impact**

### 3. Control Assessment
Identify existing controls and their effectiveness:
// turbo
```bash
python tools/custom-scripts/risk_assessment.py --new --interactive
```

### 4. Residual Risk Calculation
Calculate residual risk after controls:
```
Residual Risk = Inherent Risk × (1 - Control Effectiveness%)
```

**Risk Levels:**
- Critical (20-25): Immediate action required
- High (15-19): Priority remediation
- Medium (8-14): Planned mitigation
- Low (4-7): Monitor
- Very Low (1-3): Accept

### 5. Treatment Strategy
Recommend treatment based on residual risk:
- **Avoid**: Eliminate the risk source
- **Mitigate**: Implement additional controls
- **Transfer**: Insurance or outsourcing
- **Accept**: Document and monitor

### 6. Document Risk
Save risk to register:
// turbo
```bash
python tools/custom-scripts/risk_assessment.py --list
```

### 7. Create Treatment Plan
For risks requiring treatment:
- Define specific actions
- Assign owner
- Set due date
- Define success criteria

### 8. Monitor and Review
- Schedule periodic reviews
- Track treatment progress
- Update risk score as controls mature

## Risk Matrix Reference
```
     │  1    2    3    4    5   (Impact)
─────┼─────────────────────────
  5  │  5   10   15   20   25
  4  │  4    8   12   16   20
  3  │  3    6    9   12   15
  2  │  2    4    6    8   10
  1  │  1    2    3    4    5
(Likelihood)
```

## Output Files
- `risks/register/RISK-[ID].yaml` - Risk record
- `risks/assessments/` - Assessment documentation
- `risks/treatments/` - Treatment plans

## Related Workflows
- `/compliance` - Compliance verification
- `/control` - Control mapping
- `/gap` - Gap analysis
