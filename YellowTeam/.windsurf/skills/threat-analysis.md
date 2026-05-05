---
description: Skill for analyzing threats and attack vectors
---

# 🟡 Threat Analysis Skill

## Purpose
Analyze systems, architectures, and code for potential security threats and attack vectors.

## Capabilities

### 1. STRIDE Analysis
When analyzing a system, automatically apply STRIDE:
- **S**poofing - Identity threats
- **T**ampering - Data integrity threats
- **R**epudiation - Audit/logging threats
- **I**nformation Disclosure - Confidentiality threats
- **D**enial of Service - Availability threats
- **E**levation of Privilege - Authorization threats

### 2. Attack Vector Identification
Identify potential attack vectors:
- External attack surface
- Internal attack paths
- Supply chain risks
- Insider threats
- Third-party integrations

### 3. Vulnerability Mapping
Map threats to common vulnerabilities:
- OWASP Top 10
- CWE Top 25
- SANS Top 25
- CVE database

### 4. Risk Assessment
Calculate risk for each threat:
- Impact (High/Medium/Low)
- Likelihood (High/Medium/Low)
- Risk = Impact × Likelihood

## Usage

### Analyze Architecture
When user provides architecture description or diagram:
1. Identify all components
2. Map data flows
3. Define trust boundaries
4. Apply STRIDE to each element
5. Generate threat list with mitigations

### Analyze Code
When user provides code:
1. Identify security-sensitive operations
2. Check for common vulnerabilities
3. Assess input validation
4. Review authentication/authorization
5. Check cryptographic usage

### Analyze API
When user provides API specification:
1. Review authentication mechanisms
2. Check authorization controls
3. Assess input validation
4. Review rate limiting
5. Check for sensitive data exposure

## Output Format

### Threat Summary Table
```markdown
| ID | Threat | Category | Impact | Likelihood | Risk | Mitigation |
|----|--------|----------|--------|------------|------|------------|
| T-001 | SQL Injection | Tampering | High | Medium | High | Parameterized queries |
```

### Detailed Threat Analysis
```markdown
### T-001: SQL Injection

**Category:** Tampering
**Affected Component:** User API
**Attack Vector:** Malicious input in search parameter

**Description:**
The search endpoint accepts user input that is concatenated into SQL queries...

**Impact:** High
- Data breach
- Data manipulation
- Potential system compromise

**Likelihood:** Medium
- Requires knowledge of SQL
- Input is partially validated

**Risk:** High

**Mitigations:**
1. Use parameterized queries
2. Implement input validation
3. Apply least privilege to database user
4. Enable SQL query logging
```

## Integration with Purple Team

### Red Team Handoff
Provide threat analysis to Red Team for:
- Attack simulation planning
- Penetration testing scope
- Exploit development focus

### Blue Team Handoff
Provide threat analysis to Blue Team for:
- Detection rule development
- Monitoring configuration
- Incident response planning

## Commands
- `/analyze-threats [system]` - Full threat analysis
- `/stride [component]` - STRIDE analysis
- `/attack-vectors [system]` - Attack vector mapping
- `/risk-assess [threat]` - Risk assessment
