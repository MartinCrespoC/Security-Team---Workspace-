---
description: Skill for verifying compliance with security standards and regulations
---

# 🟡 Compliance Check Skill

## Purpose
Verify system compliance with security standards, regulations, and best practices.

## Capabilities

### 1. Standards Mapping
Map requirements to security standards:

#### NIST Cybersecurity Framework
- Identify
- Protect
- Detect
- Respond
- Recover

#### ISO 27001
- Information Security Policies
- Organization of Information Security
- Human Resource Security
- Asset Management
- Access Control
- Cryptography
- Physical Security
- Operations Security
- Communications Security
- System Development
- Supplier Relationships
- Incident Management
- Business Continuity
- Compliance

#### OWASP ASVS
- Architecture
- Authentication
- Session Management
- Access Control
- Validation
- Cryptography
- Error Handling
- Data Protection
- Communications
- Malicious Code
- Business Logic
- Files and Resources
- API Security
- Configuration

### 2. Regulatory Compliance

#### GDPR
- Lawful basis for processing
- Data subject rights
- Data protection by design
- Data breach notification
- Data protection officer
- International transfers

#### HIPAA
- Administrative safeguards
- Physical safeguards
- Technical safeguards
- Organizational requirements
- Policies and procedures

#### PCI DSS
- Network security
- Cardholder data protection
- Vulnerability management
- Access control
- Monitoring and testing
- Information security policy

#### SOC 2
- Security
- Availability
- Processing integrity
- Confidentiality
- Privacy

### 3. Compliance Assessment
Assess compliance status:
- Compliant
- Partially Compliant
- Non-Compliant
- Not Applicable

### 4. Gap Analysis
Identify compliance gaps:
- Missing controls
- Inadequate controls
- Documentation gaps
- Process gaps

## Usage

### Compliance Assessment
When user requests compliance check:
1. Identify applicable standards
2. Map current controls
3. Assess compliance status
4. Identify gaps
5. Provide remediation guidance

### Control Mapping
When user provides controls:
1. Map to standards
2. Identify coverage
3. Find gaps
4. Recommend additions

### Audit Preparation
When preparing for audit:
1. Review requirements
2. Gather evidence
3. Identify gaps
4. Create remediation plan
5. Document controls

## Output Format

### Compliance Matrix
```markdown
| Control ID | Requirement | Standard | Status | Evidence | Gap |
|------------|-------------|----------|--------|----------|-----|
| AC-1 | Access Control Policy | NIST | ✅ Compliant | Policy doc | - |
| AC-2 | Account Management | NIST | ⚠️ Partial | Process exists | No automation |
| AC-3 | Access Enforcement | NIST | ❌ Non-Compliant | - | No RBAC |
```

### Gap Analysis Report
```markdown
## Compliance Gap Analysis

### Summary
- **Standard:** NIST 800-53
- **Total Controls:** 150
- **Compliant:** 120 (80%)
- **Partial:** 20 (13%)
- **Non-Compliant:** 10 (7%)

### Critical Gaps

#### AC-3: Access Enforcement
**Requirement:** Enforce approved authorizations for logical access
**Current State:** Basic authentication only
**Gap:** No role-based access control
**Remediation:** Implement RBAC with policy engine
**Effort:** High
**Priority:** Critical

#### AU-6: Audit Review
**Requirement:** Review and analyze audit records
**Current State:** Logs collected but not reviewed
**Gap:** No automated analysis or alerting
**Remediation:** Implement SIEM with alerting
**Effort:** Medium
**Priority:** High
```

### Remediation Roadmap
```markdown
## Remediation Roadmap

### Phase 1: Critical (0-30 days)
1. Implement RBAC (AC-3)
2. Enable MFA (IA-2)
3. Encrypt data at rest (SC-28)

### Phase 2: High (30-90 days)
1. Deploy SIEM (AU-6)
2. Implement key management (SC-12)
3. Enable network segmentation (SC-7)

### Phase 3: Medium (90-180 days)
1. Automate account management (AC-2)
2. Implement DLP (SC-7)
3. Deploy vulnerability scanning (RA-5)
```

## Integration with Purple Team

### Red Team
- Validate controls through testing
- Identify control bypasses
- Verify detection capabilities

### Blue Team
- Implement required controls
- Configure monitoring
- Develop response procedures

## Commands
- `/compliance-check [standard]` - Check compliance
- `/gap-analysis [standard]` - Perform gap analysis
- `/control-map [control]` - Map control to standards
- `/audit-prep [standard]` - Prepare for audit
- `/remediation-plan [gaps]` - Create remediation plan
