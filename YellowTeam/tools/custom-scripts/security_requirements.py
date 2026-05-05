#!/usr/bin/env python3
"""
🟡 YELLOW TEAM - Security Requirements Generator
Generates comprehensive security requirements specifications
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    import typer
except ImportError:
    print("Installing required packages...")
    os.system("pip install rich typer")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    import typer

console = Console()
app = typer.Typer(help="🟡 Yellow Team Security Requirements Generator")

# Security Requirements Catalog
REQUIREMENTS_CATALOG = {
    "AUTH": {
        "name": "Authentication",
        "icon": "🔐",
        "requirements": [
            {
                "id": "AUTH-001",
                "title": "Multi-Factor Authentication",
                "description": "System SHALL implement multi-factor authentication for all user accounts",
                "priority": "Critical",
                "category": "Authentication",
                "standard": "NIST 800-63B",
                "verification": "Verify MFA is required for login; test with single factor fails"
            },
            {
                "id": "AUTH-002",
                "title": "Password Complexity",
                "description": "System SHALL enforce password complexity: minimum 12 characters, mixed case, numbers, symbols",
                "priority": "High",
                "category": "Authentication",
                "standard": "NIST 800-63B",
                "verification": "Attempt to create passwords that don't meet requirements"
            },
            {
                "id": "AUTH-003",
                "title": "Account Lockout",
                "description": "System SHALL lock accounts after 5 failed authentication attempts for 30 minutes",
                "priority": "High",
                "category": "Authentication",
                "standard": "OWASP ASVS",
                "verification": "Attempt 5+ failed logins and verify lockout"
            },
            {
                "id": "AUTH-004",
                "title": "Session Management",
                "description": "System SHALL implement secure session management with timeout after 15 minutes of inactivity",
                "priority": "High",
                "category": "Authentication",
                "standard": "OWASP ASVS",
                "verification": "Verify session expires after inactivity period"
            },
            {
                "id": "AUTH-005",
                "title": "Password Hashing",
                "description": "System SHALL hash passwords using bcrypt, scrypt, or Argon2 with appropriate work factors",
                "priority": "Critical",
                "category": "Authentication",
                "standard": "OWASP",
                "verification": "Review code/configuration for password hashing algorithm"
            },
            {
                "id": "AUTH-006",
                "title": "Credential Storage",
                "description": "System SHALL NOT store plaintext passwords or reversibly encrypted passwords",
                "priority": "Critical",
                "category": "Authentication",
                "standard": "CWE-256",
                "verification": "Database review for credential storage format"
            },
        ]
    },
    "AUTHZ": {
        "name": "Authorization",
        "icon": "🛡️",
        "requirements": [
            {
                "id": "AUTHZ-001",
                "title": "Role-Based Access Control",
                "description": "System SHALL implement role-based access control (RBAC) for all resources",
                "priority": "Critical",
                "category": "Authorization",
                "standard": "NIST AC-3",
                "verification": "Verify users can only access resources permitted by their role"
            },
            {
                "id": "AUTHZ-002",
                "title": "Least Privilege",
                "description": "System SHALL grant minimum necessary permissions to users and services",
                "priority": "Critical",
                "category": "Authorization",
                "standard": "NIST AC-6",
                "verification": "Review permission assignments for excessive privileges"
            },
            {
                "id": "AUTHZ-003",
                "title": "Separation of Duties",
                "description": "System SHALL enforce separation of duties for sensitive operations",
                "priority": "High",
                "category": "Authorization",
                "standard": "NIST AC-5",
                "verification": "Verify critical operations require multiple approvers"
            },
            {
                "id": "AUTHZ-004",
                "title": "API Authorization",
                "description": "System SHALL verify authorization for every API request",
                "priority": "Critical",
                "category": "Authorization",
                "standard": "OWASP API Security",
                "verification": "Test API endpoints with unauthorized tokens"
            },
            {
                "id": "AUTHZ-005",
                "title": "Resource-Level Permissions",
                "description": "System SHALL enforce permissions at the resource level, not just endpoint level",
                "priority": "High",
                "category": "Authorization",
                "standard": "OWASP IDOR",
                "verification": "Test access to resources owned by other users"
            },
        ]
    },
    "CRYPTO": {
        "name": "Cryptography",
        "icon": "🔒",
        "requirements": [
            {
                "id": "CRYPTO-001",
                "title": "Encryption at Rest",
                "description": "System SHALL encrypt all sensitive data at rest using AES-256 or equivalent",
                "priority": "Critical",
                "category": "Cryptography",
                "standard": "NIST SC-28",
                "verification": "Verify database/storage encryption configuration"
            },
            {
                "id": "CRYPTO-002",
                "title": "Encryption in Transit",
                "description": "System SHALL encrypt all data in transit using TLS 1.3 or TLS 1.2 with strong ciphers",
                "priority": "Critical",
                "category": "Cryptography",
                "standard": "NIST SC-8",
                "verification": "SSL/TLS scan to verify protocol and cipher configuration"
            },
            {
                "id": "CRYPTO-003",
                "title": "Key Management",
                "description": "System SHALL implement secure key management with HSM or KMS",
                "priority": "Critical",
                "category": "Cryptography",
                "standard": "NIST SC-12",
                "verification": "Review key storage and rotation procedures"
            },
            {
                "id": "CRYPTO-004",
                "title": "Key Rotation",
                "description": "System SHALL rotate encryption keys annually or upon compromise",
                "priority": "High",
                "category": "Cryptography",
                "standard": "PCI DSS 3.6",
                "verification": "Verify key rotation schedule and procedures"
            },
            {
                "id": "CRYPTO-005",
                "title": "Certificate Management",
                "description": "System SHALL use certificates from trusted CAs with minimum 2048-bit RSA or 256-bit ECC",
                "priority": "High",
                "category": "Cryptography",
                "standard": "NIST",
                "verification": "Certificate inspection for key size and CA"
            },
        ]
    },
    "DATA": {
        "name": "Data Protection",
        "icon": "📊",
        "requirements": [
            {
                "id": "DATA-001",
                "title": "Data Classification",
                "description": "System SHALL classify data according to sensitivity levels (Public, Internal, Confidential, Restricted)",
                "priority": "High",
                "category": "Data Protection",
                "standard": "ISO 27001",
                "verification": "Review data classification schema and implementation"
            },
            {
                "id": "DATA-002",
                "title": "PII Protection",
                "description": "System SHALL protect personally identifiable information (PII) with encryption and access controls",
                "priority": "Critical",
                "category": "Data Protection",
                "standard": "GDPR, CCPA",
                "verification": "Identify PII fields and verify protection measures"
            },
            {
                "id": "DATA-003",
                "title": "Data Retention",
                "description": "System SHALL retain data only for the minimum period required by business/legal needs",
                "priority": "Medium",
                "category": "Data Protection",
                "standard": "GDPR Art. 5",
                "verification": "Review retention policies and deletion procedures"
            },
            {
                "id": "DATA-004",
                "title": "Secure Deletion",
                "description": "System SHALL securely delete data when retention period expires",
                "priority": "High",
                "category": "Data Protection",
                "standard": "NIST SP 800-88",
                "verification": "Verify secure deletion procedures and tools"
            },
            {
                "id": "DATA-005",
                "title": "Data Masking",
                "description": "System SHALL mask sensitive data in non-production environments",
                "priority": "High",
                "category": "Data Protection",
                "standard": "PCI DSS",
                "verification": "Review test/dev environments for real data"
            },
        ]
    },
    "LOG": {
        "name": "Logging & Monitoring",
        "icon": "📝",
        "requirements": [
            {
                "id": "LOG-001",
                "title": "Security Event Logging",
                "description": "System SHALL log all security-relevant events including authentication, authorization, and data access",
                "priority": "Critical",
                "category": "Logging",
                "standard": "NIST AU-2",
                "verification": "Review log configuration for security events"
            },
            {
                "id": "LOG-002",
                "title": "Log Integrity",
                "description": "System SHALL protect logs from unauthorized modification or deletion",
                "priority": "High",
                "category": "Logging",
                "standard": "NIST AU-9",
                "verification": "Verify log storage permissions and integrity controls"
            },
            {
                "id": "LOG-003",
                "title": "Centralized Logging",
                "description": "System SHALL send logs to centralized logging system (SIEM)",
                "priority": "High",
                "category": "Logging",
                "standard": "NIST AU-6",
                "verification": "Verify log forwarding to SIEM"
            },
            {
                "id": "LOG-004",
                "title": "Log Retention",
                "description": "System SHALL retain security logs for minimum 90 days online, 1 year archived",
                "priority": "Medium",
                "category": "Logging",
                "standard": "PCI DSS 10.7",
                "verification": "Review log retention configuration"
            },
            {
                "id": "LOG-005",
                "title": "Real-time Alerting",
                "description": "System SHALL generate real-time alerts for critical security events",
                "priority": "High",
                "category": "Logging",
                "standard": "NIST SI-4",
                "verification": "Test alert generation for security events"
            },
        ]
    },
    "NET": {
        "name": "Network Security",
        "icon": "🌐",
        "requirements": [
            {
                "id": "NET-001",
                "title": "Network Segmentation",
                "description": "System SHALL implement network segmentation between security zones",
                "priority": "High",
                "category": "Network",
                "standard": "NIST SC-7",
                "verification": "Review network architecture and firewall rules"
            },
            {
                "id": "NET-002",
                "title": "Firewall Configuration",
                "description": "System SHALL implement deny-by-default firewall rules",
                "priority": "High",
                "category": "Network",
                "standard": "NIST SC-7",
                "verification": "Review firewall ruleset for default deny"
            },
            {
                "id": "NET-003",
                "title": "Web Application Firewall",
                "description": "System SHALL deploy WAF for all public-facing web applications",
                "priority": "High",
                "category": "Network",
                "standard": "OWASP",
                "verification": "Verify WAF deployment and rule configuration"
            },
            {
                "id": "NET-004",
                "title": "DDoS Protection",
                "description": "System SHALL implement DDoS protection for public-facing services",
                "priority": "Medium",
                "category": "Network",
                "standard": "NIST SC-5",
                "verification": "Review DDoS mitigation capabilities"
            },
            {
                "id": "NET-005",
                "title": "Intrusion Detection",
                "description": "System SHALL deploy intrusion detection/prevention systems",
                "priority": "Medium",
                "category": "Network",
                "standard": "NIST SI-4",
                "verification": "Verify IDS/IPS deployment and monitoring"
            },
        ]
    },
    "APP": {
        "name": "Application Security",
        "icon": "💻",
        "requirements": [
            {
                "id": "APP-001",
                "title": "Input Validation",
                "description": "System SHALL validate all input data on the server side",
                "priority": "Critical",
                "category": "Application",
                "standard": "OWASP ASVS",
                "verification": "Test with malformed/malicious input"
            },
            {
                "id": "APP-002",
                "title": "Output Encoding",
                "description": "System SHALL encode output data to prevent injection attacks",
                "priority": "Critical",
                "category": "Application",
                "standard": "OWASP ASVS",
                "verification": "Test for XSS vulnerabilities"
            },
            {
                "id": "APP-003",
                "title": "SQL Injection Prevention",
                "description": "System SHALL use parameterized queries or ORM to prevent SQL injection",
                "priority": "Critical",
                "category": "Application",
                "standard": "CWE-89",
                "verification": "Code review and SQL injection testing"
            },
            {
                "id": "APP-004",
                "title": "CSRF Protection",
                "description": "System SHALL implement CSRF tokens for state-changing operations",
                "priority": "High",
                "category": "Application",
                "standard": "OWASP ASVS",
                "verification": "Test for CSRF vulnerabilities"
            },
            {
                "id": "APP-005",
                "title": "Security Headers",
                "description": "System SHALL implement security headers (CSP, HSTS, X-Frame-Options, etc.)",
                "priority": "High",
                "category": "Application",
                "standard": "OWASP",
                "verification": "Scan for security header configuration"
            },
            {
                "id": "APP-006",
                "title": "Dependency Scanning",
                "description": "System SHALL scan dependencies for known vulnerabilities",
                "priority": "High",
                "category": "Application",
                "standard": "OWASP",
                "verification": "Review dependency scanning results"
            },
        ]
    },
    "CONF": {
        "name": "Configuration",
        "icon": "⚙️",
        "requirements": [
            {
                "id": "CONF-001",
                "title": "Secure Defaults",
                "description": "System SHALL use secure default configurations",
                "priority": "High",
                "category": "Configuration",
                "standard": "CIS Benchmarks",
                "verification": "Compare configuration against CIS benchmarks"
            },
            {
                "id": "CONF-002",
                "title": "Secrets Management",
                "description": "System SHALL store secrets in dedicated secrets management solution",
                "priority": "Critical",
                "category": "Configuration",
                "standard": "OWASP",
                "verification": "Review secrets storage and access"
            },
            {
                "id": "CONF-003",
                "title": "Configuration Hardening",
                "description": "System SHALL disable unnecessary services, ports, and features",
                "priority": "High",
                "category": "Configuration",
                "standard": "CIS Benchmarks",
                "verification": "Review running services and open ports"
            },
            {
                "id": "CONF-004",
                "title": "Patch Management",
                "description": "System SHALL apply security patches within 30 days (critical within 7 days)",
                "priority": "Critical",
                "category": "Configuration",
                "standard": "NIST SI-2",
                "verification": "Review patch status and procedures"
            },
        ]
    },
}


class SecurityRequirements:
    """Security Requirements Specification"""

    def __init__(self, project_name: str, version: str = "1.0"):
        self.project_name = project_name
        self.version = version
        self.created = datetime.now().isoformat()
        self.author = os.getenv("USER", "Yellow Team")
        self.requirements: List[Dict] = []
        self.custom_requirements: List[Dict] = []

    def add_requirement(self, req: Dict):
        """Add a requirement from catalog"""
        self.requirements.append(req)

    def add_custom_requirement(self, id_: str, title: str, description: str,
                               priority: str, category: str, verification: str):
        """Add a custom requirement"""
        self.custom_requirements.append({
            "id": id_,
            "title": title,
            "description": description,
            "priority": priority,
            "category": category,
            "verification": verification,
            "standard": "Custom"
        })

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "project_name": self.project_name,
            "version": self.version,
            "created": self.created,
            "author": self.author,
            "requirements": self.requirements + self.custom_requirements
        }

    def to_markdown(self) -> str:
        """Generate Markdown specification"""
        all_reqs = self.requirements + self.custom_requirements

        # Count by priority
        priority_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for req in all_reqs:
            priority_counts[req.get("priority", "Medium")] += 1

        md = f"""# 🟡 Security Requirements Specification

## Document Information

| Field | Value |
|-------|-------|
| **Project** | {self.project_name} |
| **Version** | {self.version} |
| **Created** | {self.created} |
| **Author** | {self.author} |
| **Total Requirements** | {len(all_reqs)} |

## Executive Summary

This document specifies security requirements for **{self.project_name}**.

### Requirements by Priority

| Priority | Count |
|----------|-------|
| 🔴 Critical | {priority_counts['Critical']} |
| 🟠 High | {priority_counts['High']} |
| 🟡 Medium | {priority_counts['Medium']} |
| 🟢 Low | {priority_counts['Low']} |

---

## Security Requirements

"""
        # Group by category
        categories = {}
        for req in all_reqs:
            cat = req.get("category", "Other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(req)

        for category, reqs in categories.items():
            # Find icon
            icon = "📋"
            for cat_key, cat_info in REQUIREMENTS_CATALOG.items():
                if cat_info["name"] == category:
                    icon = cat_info["icon"]
                    break

            md += f"### {icon} {category}\n\n"

            for req in reqs:
                priority_emoji = {
                    "Critical": "🔴",
                    "High": "🟠",
                    "Medium": "🟡",
                    "Low": "🟢"
                }.get(req.get("priority", "Medium"), "⚪")

                md += f"""#### {req['id']}: {req['title']}

| Field | Value |
|-------|-------|
| **Priority** | {priority_emoji} {req.get('priority', 'Medium')} |
| **Standard** | {req.get('standard', 'N/A')} |

**Requirement:** {req['description']}

**Verification:** {req.get('verification', 'To be defined')}

---

"""

        md += """## Traceability Matrix

| Requirement | Category | Priority | Standard | Status |
|-------------|----------|----------|----------|--------|
"""
        for req in all_reqs:
            md += f"| {req['id']} | {req.get('category', 'N/A')} | {req.get('priority', 'Medium')} | {req.get('standard', 'N/A')} | ⏳ Pending |\n"

        md += f"""
## Compliance Mapping

### Standards Coverage

| Standard | Requirements |
|----------|--------------|
| NIST | {len([r for r in all_reqs if 'NIST' in r.get('standard', '')])} |
| OWASP | {len([r for r in all_reqs if 'OWASP' in r.get('standard', '')])} |
| PCI DSS | {len([r for r in all_reqs if 'PCI' in r.get('standard', '')])} |
| GDPR | {len([r for r in all_reqs if 'GDPR' in r.get('standard', '')])} |
| ISO 27001 | {len([r for r in all_reqs if 'ISO' in r.get('standard', '')])} |
| CIS | {len([r for r in all_reqs if 'CIS' in r.get('standard', '')])} |

## Appendix

### Definitions

| Term | Definition |
|------|------------|
| SHALL | Mandatory requirement |
| SHOULD | Recommended requirement |
| MAY | Optional requirement |

### Priority Definitions

| Priority | Definition |
|----------|------------|
| 🔴 Critical | Must be implemented before production |
| 🟠 High | Should be implemented before production |
| 🟡 Medium | Should be implemented within 90 days |
| 🟢 Low | Should be implemented within 180 days |

---
*Generated by Yellow Team Security Requirements Generator*
*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return md


def print_banner():
    """Print Yellow Team banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🟡 YELLOW TEAM - SECURITY REQUIREMENTS GENERATOR                            ║
║                                                                               ║
║   Generate Comprehensive Security Requirements                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    console.print(Panel(banner, style="yellow"))


def interactive_mode():
    """Run interactive requirements generation"""
    print_banner()

    console.print("\n[bold yellow]📋 Project Information[/bold yellow]\n")

    project_name = Prompt.ask("Project name")
    version = Prompt.ask("Version", default="1.0")

    spec = SecurityRequirements(project_name, version)

    console.print("\n[bold yellow]📝 Select Requirements Categories[/bold yellow]\n")

    for cat_key, cat_info in REQUIREMENTS_CATALOG.items():
        console.print(f"\n{cat_info['icon']} [bold]{cat_info['name']}[/bold]")
        console.print(f"   {len(cat_info['requirements'])} requirements available")

        if Confirm.ask(f"Include {cat_info['name']} requirements?"):
            # Show individual requirements
            for req in cat_info["requirements"]:
                priority_emoji = {
                    "Critical": "🔴",
                    "High": "🟠",
                    "Medium": "🟡",
                    "Low": "🟢"
                }.get(req["priority"], "⚪")

                console.print(f"   {priority_emoji} [{req['id']}] {req['title']}")

            if Confirm.ask("Include all requirements from this category?"):
                for req in cat_info["requirements"]:
                    spec.add_requirement(req)
            else:
                for req in cat_info["requirements"]:
                    if Confirm.ask(f"Include {req['id']}: {req['title']}?"):
                        spec.add_requirement(req)

    # Custom requirements
    console.print("\n[bold yellow]➕ Custom Requirements[/bold yellow]")

    while Confirm.ask("Add custom requirement?"):
        id_ = Prompt.ask("Requirement ID (e.g., CUSTOM-001)")
        title = Prompt.ask("Title")
        description = Prompt.ask("Description (use SHALL/SHOULD/MAY)")
        priority = Prompt.ask("Priority", choices=["Critical", "High", "Medium", "Low"])
        category = Prompt.ask("Category")
        verification = Prompt.ask("Verification method")

        spec.add_custom_requirement(id_, title, description, priority, category, verification)

    # Generate output
    console.print("\n[bold yellow]📄 Generating Requirements Specification...[/bold yellow]\n")

    script_dir = Path(__file__).parent.parent.parent
    output_dir = script_dir / "requirements"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = project_name.lower().replace(" ", "-")

    # Save Markdown
    md_file = output_dir / f"{safe_name}-security-requirements-{timestamp}.md"
    with open(md_file, "w") as f:
        f.write(spec.to_markdown())
    console.print(f"[green]✓[/green] Markdown saved: {md_file}")

    # Save JSON
    json_file = output_dir / f"{safe_name}-security-requirements-{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(spec.to_dict(), f, indent=2)
    console.print(f"[green]✓[/green] JSON saved: {json_file}")

    # Display summary
    all_reqs = spec.requirements + spec.custom_requirements

    summary_table = Table(title="Requirements Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Count", style="yellow")

    summary_table.add_row("Total Requirements", str(len(all_reqs)))
    summary_table.add_row("Critical", str(len([r for r in all_reqs if r.get("priority") == "Critical"])))
    summary_table.add_row("High", str(len([r for r in all_reqs if r.get("priority") == "High"])))
    summary_table.add_row("Medium", str(len([r for r in all_reqs if r.get("priority") == "Medium"])))
    summary_table.add_row("Low", str(len([r for r in all_reqs if r.get("priority") == "Low"])))

    console.print(summary_table)


@app.command()
def generate(
    project: str = typer.Option(None, "--project", "-p", help="Project name"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
    all_reqs: bool = typer.Option(False, "--all", "-a", help="Include all requirements"),
):
    """Generate security requirements specification"""
    if interactive or not project:
        interactive_mode()
    elif all_reqs and project:
        console.print(f"[yellow]Generating all requirements for: {project}[/yellow]")
        spec = SecurityRequirements(project)

        for cat_info in REQUIREMENTS_CATALOG.values():
            for req in cat_info["requirements"]:
                spec.add_requirement(req)

        script_dir = Path(__file__).parent.parent.parent
        output_dir = script_dir / "requirements"
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = project.lower().replace(" ", "-")

        md_file = output_dir / f"{safe_name}-security-requirements-{timestamp}.md"
        with open(md_file, "w") as f:
            f.write(spec.to_markdown())
        console.print(f"[green]✓[/green] Generated: {md_file}")
    else:
        console.print("[yellow]Use --interactive or --all flag[/yellow]")


@app.command()
def catalog():
    """Display requirements catalog"""
    print_banner()

    for cat_key, cat_info in REQUIREMENTS_CATALOG.items():
        table = Table(title=f"{cat_info['icon']} {cat_info['name']}")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Priority", style="yellow")
        table.add_column("Standard", style="blue")

        for req in cat_info["requirements"]:
            priority_color = {
                "Critical": "red",
                "High": "orange1",
                "Medium": "yellow",
                "Low": "green"
            }.get(req["priority"], "white")

            table.add_row(
                req["id"],
                req["title"],
                f"[{priority_color}]{req['priority']}[/{priority_color}]",
                req["standard"]
            )

        console.print(table)
        console.print()


@app.command()
def template(
    output: str = typer.Option(".", "--output", "-o", help="Output directory"),
):
    """Generate requirements template"""
    template_content = """# Security Requirements Template

## Project Information
- **Project:**
- **Version:**
- **Date:**
- **Author:**

## Requirements

### Authentication
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| AUTH-001 | System SHALL implement MFA | Critical | |

### Authorization
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| AUTHZ-001 | System SHALL implement RBAC | Critical | |

### Data Protection
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| DATA-001 | System SHALL encrypt data at rest | Critical | |

### Logging
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| LOG-001 | System SHALL log security events | Critical | |

## Traceability
| Requirement | Threat | Control | Test |
|-------------|--------|---------|------|
| | | | |
"""
    output_path = Path(output) / "security-requirements-template.md"
    with open(output_path, "w") as f:
        f.write(template_content)
    console.print(f"[green]✓[/green] Template saved: {output_path}")


if __name__ == "__main__":
    app()
