# PCI-DSS v4.0 Framework Reference

## Overview

PCI-DSS (Payment Card Industry Data Security Standard) is a security standard for organizations that handle credit card data.

## 12 Requirements

### Build and Maintain a Secure Network

| Req | Name | Sub-Requirements |
|-----|------|------------------|
| 1 | Network Security Controls | 1.1-1.5 |
| 2 | Secure Configurations | 2.1-2.3 |

### Protect Account Data

| Req | Name | Sub-Requirements |
|-----|------|------------------|
| 3 | Protect Stored Account Data | 3.1-3.7 |
| 4 | Protect Cardholder Data in Transit | 4.1-4.2 |

### Maintain a Vulnerability Management Program

| Req | Name | Sub-Requirements |
|-----|------|------------------|
| 5 | Protect Against Malware | 5.1-5.4 |
| 6 | Develop Secure Systems | 6.1-6.5 |

### Implement Strong Access Control

| Req | Name | Sub-Requirements |
|-----|------|------------------|
| 7 | Restrict Access | 7.1-7.3 |
| 8 | Identify and Authenticate | 8.1-8.6 |
| 9 | Restrict Physical Access | 9.1-9.5 |

### Regularly Monitor and Test Networks

| Req | Name | Sub-Requirements |
|-----|------|------------------|
| 10 | Log and Monitor | 10.1-10.7 |
| 11 | Test Security | 11.1-11.6 |

### Maintain an Information Security Policy

| Req | Name | Sub-Requirements |
|-----|------|------------------|
| 12 | Support Security Policies | 12.1-12.10 |

## SAQ Types

| SAQ | Description | Requirements |
|-----|-------------|--------------|
| A | Card-not-present, outsourced | ~20 |
| A-EP | E-commerce, partial outsource | ~140 |
| B | Imprint or standalone dial-out | ~40 |
| B-IP | Standalone IP terminals | ~80 |
| C | Payment application systems | ~160 |
| C-VT | Virtual terminal | ~80 |
| D | All other merchants | ~300+ |
| D-SP | Service providers | ~400+ |

## Key Changes in v4.0

1. **Customized Approach**: Alternative to defined approach
2. **Authentication**: Enhanced MFA requirements (8.4)
3. **E-commerce**: New requirements for payment page scripts (6.4.3)
4. **Risk Assessment**: Targeted risk analysis requirements
5. **Encryption**: Updated cryptographic requirements

## Compliance Levels

| Level | Transactions/Year | Validation |
|-------|-------------------|------------|
| 1 | >6 million | Annual ROC by QSA |
| 2 | 1-6 million | Annual SAQ |
| 3 | 20K-1 million | Annual SAQ |
| 4 | <20K | Annual SAQ |

## Key Dates

- **March 2024**: v4.0 becomes mandatory
- **March 2025**: Future-dated requirements become mandatory

## Resources

- [PCI SSC Website](https://www.pcisecuritystandards.org)
- [PCI DSS v4.0 Document](https://www.pcisecuritystandards.org/document_library)
