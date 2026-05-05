# SOC 2 Type II Framework Reference

## Overview

SOC 2 (Service Organization Control 2) is an auditing framework developed by AICPA for service organizations to demonstrate their security controls.

## Trust Services Criteria

### Common Criteria (CC) - Required

| Category | Name | Points of Focus |
|----------|------|-----------------|
| CC1 | Control Environment | 5 |
| CC2 | Communication and Information | 3 |
| CC3 | Risk Assessment | 4 |
| CC4 | Monitoring Activities | 2 |
| CC5 | Control Activities | 3 |
| CC6 | Logical and Physical Access | 8 |
| CC7 | System Operations | 5 |
| CC8 | Change Management | 1 |
| CC9 | Risk Mitigation | 2 |

### Additional Criteria (Optional)

| Category | Name | When Required |
|----------|------|---------------|
| A | Availability | When availability is in scope |
| PI | Processing Integrity | When processing integrity is in scope |
| C | Confidentiality | When confidentiality is in scope |
| P | Privacy | When privacy is in scope |

## Type I vs Type II

| Aspect | Type I | Type II |
|--------|--------|---------|
| Point in Time | Yes | No |
| Period of Time | No | Yes (min 6 months) |
| Design Effectiveness | Yes | Yes |
| Operating Effectiveness | No | Yes |

## Key Requirements

### CC6 - Logical and Physical Access

- CC6.1: Logical access security software
- CC6.2: New user registration
- CC6.3: User access removal
- CC6.4: Access review
- CC6.5: Physical access restrictions
- CC6.6: Logical access restrictions
- CC6.7: Data transmission protection
- CC6.8: Malware prevention

### CC7 - System Operations

- CC7.1: Detection of security events
- CC7.2: Monitoring for anomalies
- CC7.3: Security event evaluation
- CC7.4: Incident response
- CC7.5: Recovery from incidents

## Evidence Requirements

- Control descriptions
- Testing procedures
- Sample selections
- Exception documentation
- Management assertions

## Audit Timeline

1. **Readiness Assessment** (2-4 weeks)
2. **Gap Remediation** (4-12 weeks)
3. **Type I Audit** (2-4 weeks)
4. **Observation Period** (6-12 months)
5. **Type II Audit** (4-6 weeks)

## Resources

- [AICPA SOC 2 Guide](https://www.aicpa.org/soc2)
- [Trust Services Criteria](https://www.aicpa.org/trustservicescriteria)
