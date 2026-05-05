---
description: Perform a comprehensive security review of system architecture
---

# 🟡 Architecture Security Review Workflow

## Overview
This workflow guides you through performing a comprehensive security review of a system architecture.

## Steps

### 1. Understand the System
Gather information about:
- System purpose and scope
- Architecture diagrams
- Technology stack
- Data sensitivity
- Compliance requirements
- Existing security controls

### 2. Identify Components
Document all system components:

| Component | Type | Technology | Description |
|-----------|------|------------|-------------|
| Web App | Frontend | React | User interface |
| API | Backend | Node.js | Business logic |
| Database | Storage | PostgreSQL | Data persistence |
| Cache | Storage | Redis | Session/cache |

### 3. Security Checklist Evaluation

#### 🔐 Authentication
- [ ] Multi-factor authentication
- [ ] Strong password policy
- [ ] Account lockout mechanism
- [ ] Secure session management
- [ ] Password hashing (bcrypt/argon2)

#### 🛡️ Authorization
- [ ] Role-based access control
- [ ] Least privilege principle
- [ ] API authorization checks
- [ ] Resource-level permissions

#### 🔒 Data Protection
- [ ] Encryption at rest (AES-256)
- [ ] Encryption in transit (TLS 1.3)
- [ ] Key management system
- [ ] Data classification
- [ ] PII/PHI handling

#### 🌐 Network Security
- [ ] Network segmentation
- [ ] Firewall configuration
- [ ] WAF deployment
- [ ] DDoS protection
- [ ] IDS/IPS

#### 📊 Logging & Monitoring
- [ ] Centralized logging
- [ ] Security event logging
- [ ] Real-time alerting
- [ ] SIEM integration
- [ ] Log retention

#### 💻 Application Security
- [ ] Input validation
- [ ] Output encoding
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Security headers

### 4. Document Findings
For each finding, document:
- Finding ID
- Severity (Critical/High/Medium/Low)
- Title
- Description
- Affected component
- Business impact
- Recommendation
- Remediation effort

### 5. Generate Report
// turbo
Run the architecture review tool:
```bash
python tools/custom-scripts/architecture_review.py --interactive
```

### 6. Risk Assessment
Calculate overall risk:
- Count findings by severity
- Assess business impact
- Determine risk rating
- Prioritize remediation

### 7. Recommendations
Provide actionable recommendations:
1. **Immediate** - Critical/High findings
2. **Short-term** - Medium findings (30-60 days)
3. **Long-term** - Low findings, improvements

## Output Files
- `reviews/[system]-security-review-[date].md` - Markdown report
- `reviews/[system]-security-review-[date].json` - JSON data

## Review Checklist Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY REVIEW CHECKLIST                    │
├─────────────────────────────────────────────────────────────────┤
│ □ Authentication controls verified                              │
│ □ Authorization mechanisms reviewed                             │
│ □ Data protection assessed                                      │
│ □ Network security evaluated                                    │
│ □ Logging and monitoring checked                                │
│ □ Application security tested                                   │
│ □ Infrastructure security reviewed                              │
│ □ Compliance requirements mapped                                │
│ □ Findings documented                                           │
│ □ Recommendations provided                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Tips
- Review architecture diagrams before starting
- Interview developers and operators
- Check for security documentation
- Validate controls with evidence
- Consider threat model findings
