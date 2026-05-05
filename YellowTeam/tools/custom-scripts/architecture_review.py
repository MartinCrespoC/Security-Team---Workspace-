#!/usr/bin/env python3
"""
🟡 YELLOW TEAM - Architecture Security Review Tool
Performs comprehensive security reviews of system architectures
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
    from rich.progress import Progress, SpinnerColumn, TextColumn
    import typer
except ImportError:
    print("Installing required packages...")
    os.system("pip install rich typer")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    import typer

console = Console()
app = typer.Typer(help="🟡 Yellow Team Architecture Security Review")

# Security Review Checklist
REVIEW_CHECKLIST = {
    "authentication": {
        "name": "Authentication",
        "icon": "🔐",
        "checks": [
            {"id": "AUTH-001", "check": "Multi-factor authentication implemented", "severity": "High"},
            {"id": "AUTH-002", "check": "Strong password policy enforced", "severity": "High"},
            {"id": "AUTH-003", "check": "Account lockout mechanism", "severity": "Medium"},
            {"id": "AUTH-004", "check": "Secure session management", "severity": "High"},
            {"id": "AUTH-005", "check": "Password hashing (bcrypt/argon2)", "severity": "Critical"},
            {"id": "AUTH-006", "check": "Credential storage security", "severity": "Critical"},
            {"id": "AUTH-007", "check": "OAuth/OIDC implementation", "severity": "Medium"},
            {"id": "AUTH-008", "check": "Token expiration and rotation", "severity": "High"},
        ]
    },
    "authorization": {
        "name": "Authorization",
        "icon": "🛡️",
        "checks": [
            {"id": "AUTHZ-001", "check": "Role-based access control (RBAC)", "severity": "High"},
            {"id": "AUTHZ-002", "check": "Least privilege principle", "severity": "High"},
            {"id": "AUTHZ-003", "check": "Separation of duties", "severity": "Medium"},
            {"id": "AUTHZ-004", "check": "Resource-level permissions", "severity": "High"},
            {"id": "AUTHZ-005", "check": "API authorization checks", "severity": "Critical"},
            {"id": "AUTHZ-006", "check": "Admin access controls", "severity": "Critical"},
            {"id": "AUTHZ-007", "check": "Privilege escalation prevention", "severity": "Critical"},
        ]
    },
    "data_protection": {
        "name": "Data Protection",
        "icon": "🔒",
        "checks": [
            {"id": "DATA-001", "check": "Encryption at rest (AES-256)", "severity": "Critical"},
            {"id": "DATA-002", "check": "Encryption in transit (TLS 1.3)", "severity": "Critical"},
            {"id": "DATA-003", "check": "Key management system", "severity": "Critical"},
            {"id": "DATA-004", "check": "Data classification implemented", "severity": "High"},
            {"id": "DATA-005", "check": "PII/PHI handling procedures", "severity": "Critical"},
            {"id": "DATA-006", "check": "Data retention policies", "severity": "Medium"},
            {"id": "DATA-007", "check": "Secure data deletion", "severity": "High"},
            {"id": "DATA-008", "check": "Backup encryption", "severity": "High"},
        ]
    },
    "network_security": {
        "name": "Network Security",
        "icon": "🌐",
        "checks": [
            {"id": "NET-001", "check": "Network segmentation", "severity": "High"},
            {"id": "NET-002", "check": "Firewall rules configured", "severity": "High"},
            {"id": "NET-003", "check": "WAF implemented", "severity": "High"},
            {"id": "NET-004", "check": "DDoS protection", "severity": "Medium"},
            {"id": "NET-005", "check": "VPN for remote access", "severity": "High"},
            {"id": "NET-006", "check": "IDS/IPS deployed", "severity": "Medium"},
            {"id": "NET-007", "check": "DNS security (DNSSEC)", "severity": "Medium"},
            {"id": "NET-008", "check": "Certificate management", "severity": "High"},
        ]
    },
    "logging_monitoring": {
        "name": "Logging & Monitoring",
        "icon": "📊",
        "checks": [
            {"id": "LOG-001", "check": "Centralized logging", "severity": "High"},
            {"id": "LOG-002", "check": "Security event logging", "severity": "Critical"},
            {"id": "LOG-003", "check": "Log integrity protection", "severity": "High"},
            {"id": "LOG-004", "check": "Real-time alerting", "severity": "High"},
            {"id": "LOG-005", "check": "SIEM integration", "severity": "Medium"},
            {"id": "LOG-006", "check": "Audit trail for sensitive ops", "severity": "Critical"},
            {"id": "LOG-007", "check": "Log retention (90+ days)", "severity": "Medium"},
            {"id": "LOG-008", "check": "Anomaly detection", "severity": "Medium"},
        ]
    },
    "application_security": {
        "name": "Application Security",
        "icon": "💻",
        "checks": [
            {"id": "APP-001", "check": "Input validation", "severity": "Critical"},
            {"id": "APP-002", "check": "Output encoding", "severity": "High"},
            {"id": "APP-003", "check": "SQL injection prevention", "severity": "Critical"},
            {"id": "APP-004", "check": "XSS prevention", "severity": "Critical"},
            {"id": "APP-005", "check": "CSRF protection", "severity": "High"},
            {"id": "APP-006", "check": "Security headers configured", "severity": "High"},
            {"id": "APP-007", "check": "Dependency scanning", "severity": "High"},
            {"id": "APP-008", "check": "Secure error handling", "severity": "Medium"},
        ]
    },
    "infrastructure": {
        "name": "Infrastructure Security",
        "icon": "🏗️",
        "checks": [
            {"id": "INF-001", "check": "Hardened OS configurations", "severity": "High"},
            {"id": "INF-002", "check": "Patch management process", "severity": "Critical"},
            {"id": "INF-003", "check": "Container security", "severity": "High"},
            {"id": "INF-004", "check": "Secrets management", "severity": "Critical"},
            {"id": "INF-005", "check": "Infrastructure as Code security", "severity": "High"},
            {"id": "INF-006", "check": "Cloud security posture", "severity": "High"},
            {"id": "INF-007", "check": "Backup and recovery", "severity": "High"},
            {"id": "INF-008", "check": "Disaster recovery plan", "severity": "Medium"},
        ]
    },
    "compliance": {
        "name": "Compliance",
        "icon": "📋",
        "checks": [
            {"id": "COMP-001", "check": "Regulatory requirements identified", "severity": "High"},
            {"id": "COMP-002", "check": "Privacy policy implemented", "severity": "High"},
            {"id": "COMP-003", "check": "Data processing agreements", "severity": "Medium"},
            {"id": "COMP-004", "check": "Third-party risk assessment", "severity": "High"},
            {"id": "COMP-005", "check": "Security documentation", "severity": "Medium"},
            {"id": "COMP-006", "check": "Incident response plan", "severity": "High"},
            {"id": "COMP-007", "check": "Business continuity plan", "severity": "Medium"},
        ]
    },
}


class ArchitectureReview:
    """Architecture Security Review"""

    def __init__(self, system_name: str, reviewer: str = ""):
        self.system_name = system_name
        self.reviewer = reviewer or os.getenv("USER", "Yellow Team")
        self.review_date = datetime.now().isoformat()
        self.findings: List[Dict] = []
        self.checklist_results: Dict[str, Dict] = {}
        self.components: List[Dict] = []
        self.overall_score = 0

    def add_component(self, name: str, type_: str, description: str = ""):
        """Add a component to review"""
        self.components.append({
            "name": name,
            "type": type_,
            "description": description
        })

    def evaluate_check(self, category: str, check_id: str, status: str, notes: str = ""):
        """Evaluate a security check"""
        if category not in self.checklist_results:
            self.checklist_results[category] = {}

        self.checklist_results[category][check_id] = {
            "status": status,  # Pass, Fail, N/A, Partial
            "notes": notes
        }

    def add_finding(self, severity: str, title: str, description: str,
                    affected_component: str, recommendation: str):
        """Add a security finding"""
        finding_id = f"FIND-{len(self.findings) + 1:03d}"
        self.findings.append({
            "id": finding_id,
            "severity": severity,
            "title": title,
            "description": description,
            "affected_component": affected_component,
            "recommendation": recommendation,
            "status": "Open"
        })
        return finding_id

    def calculate_score(self) -> int:
        """Calculate overall security score"""
        total_checks = 0
        passed_checks = 0

        for category, results in self.checklist_results.items():
            for check_id, result in results.items():
                if result["status"] != "N/A":
                    total_checks += 1
                    if result["status"] == "Pass":
                        passed_checks += 1
                    elif result["status"] == "Partial":
                        passed_checks += 0.5

        if total_checks > 0:
            self.overall_score = int((passed_checks / total_checks) * 100)
        return self.overall_score

    def get_risk_rating(self) -> str:
        """Get overall risk rating based on findings"""
        critical = len([f for f in self.findings if f["severity"] == "Critical"])
        high = len([f for f in self.findings if f["severity"] == "High"])

        if critical > 0:
            return "Critical"
        elif high > 2:
            return "High"
        elif high > 0:
            return "Medium"
        else:
            return "Low"

    def to_markdown(self) -> str:
        """Generate Markdown report"""
        score = self.calculate_score()
        risk_rating = self.get_risk_rating()

        risk_emoji = {
            "Critical": "🔴",
            "High": "🟠",
            "Medium": "🟡",
            "Low": "🟢"
        }

        md = f"""# 🟡 Architecture Security Review

## Executive Summary

| Field | Value |
|-------|-------|
| **System** | {self.system_name} |
| **Reviewer** | {self.reviewer} |
| **Date** | {self.review_date} |
| **Security Score** | {score}% |
| **Risk Rating** | {risk_emoji.get(risk_rating, '⚪')} {risk_rating} |

## Components Reviewed

| Component | Type | Description |
|-----------|------|-------------|
"""
        for comp in self.components:
            md += f"| {comp['name']} | {comp['type']} | {comp['description']} |\n"

        md += "\n## Security Checklist Results\n\n"

        for category, info in REVIEW_CHECKLIST.items():
            md += f"### {info['icon']} {info['name']}\n\n"
            md += "| ID | Check | Severity | Status | Notes |\n"
            md += "|----|-------|----------|--------|-------|\n"

            for check in info["checks"]:
                result = self.checklist_results.get(category, {}).get(check["id"], {})
                status = result.get("status", "Not Evaluated")
                notes = result.get("notes", "")

                status_emoji = {
                    "Pass": "✅",
                    "Fail": "❌",
                    "Partial": "⚠️",
                    "N/A": "➖"
                }.get(status, "❓")

                md += f"| {check['id']} | {check['check']} | {check['severity']} | {status_emoji} {status} | {notes} |\n"

            md += "\n"

        md += "## Findings\n\n"

        if self.findings:
            # Group by severity
            for severity in ["Critical", "High", "Medium", "Low"]:
                severity_findings = [f for f in self.findings if f["severity"] == severity]
                if severity_findings:
                    md += f"### {risk_emoji.get(severity, '⚪')} {severity} Severity\n\n"
                    for finding in severity_findings:
                        md += f"""#### {finding['id']}: {finding['title']}

**Affected Component:** {finding['affected_component']}

**Description:** {finding['description']}

**Recommendation:** {finding['recommendation']}

**Status:** {finding['status']}

---

"""
        else:
            md += "*No findings identified*\n\n"

        md += f"""## Risk Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | {len([f for f in self.findings if f['severity'] == 'Critical'])} |
| 🟠 High | {len([f for f in self.findings if f['severity'] == 'High'])} |
| 🟡 Medium | {len([f for f in self.findings if f['severity'] == 'Medium'])} |
| 🟢 Low | {len([f for f in self.findings if f['severity'] == 'Low'])} |

## Recommendations

### Immediate Actions (Critical/High)
"""
        critical_high = [f for f in self.findings if f["severity"] in ["Critical", "High"]]
        for i, finding in enumerate(critical_high, 1):
            md += f"{i}. **{finding['title']}**: {finding['recommendation']}\n"

        md += """
### Short-term Actions (Medium)
"""
        medium = [f for f in self.findings if f["severity"] == "Medium"]
        for i, finding in enumerate(medium, 1):
            md += f"{i}. **{finding['title']}**: {finding['recommendation']}\n"

        md += f"""
## Conclusion

The architecture review identified **{len(self.findings)}** security findings with an overall security score of **{score}%**.

The system's current risk rating is **{risk_rating}**.

---
*Generated by Yellow Team Architecture Review Tool*
*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return md

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "system_name": self.system_name,
            "reviewer": self.reviewer,
            "review_date": self.review_date,
            "components": self.components,
            "checklist_results": self.checklist_results,
            "findings": self.findings,
            "overall_score": self.calculate_score(),
            "risk_rating": self.get_risk_rating()
        }


def print_banner():
    """Print Yellow Team banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🟡 YELLOW TEAM - ARCHITECTURE SECURITY REVIEW                               ║
║                                                                               ║
║   Comprehensive Security Assessment Tool                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    console.print(Panel(banner, style="yellow"))


def interactive_review():
    """Run interactive architecture review"""
    print_banner()

    console.print("\n[bold yellow]📋 System Information[/bold yellow]\n")

    system_name = Prompt.ask("System name")
    reviewer = Prompt.ask("Reviewer name", default=os.getenv("USER", ""))

    review = ArchitectureReview(system_name, reviewer)

    # Add components
    console.print("\n[bold yellow]🧩 Components to Review[/bold yellow]")
    console.print("Add components (type 'done' when finished)\n")

    while True:
        comp_name = Prompt.ask("Component name (or 'done')")
        if comp_name.lower() == "done":
            break
        comp_type = Prompt.ask("Type", choices=["Web App", "API", "Database", "Service", "Infrastructure", "Network"])
        comp_desc = Prompt.ask("Description", default="")
        review.add_component(comp_name, comp_type, comp_desc)

    # Security checklist
    console.print("\n[bold yellow]📝 Security Checklist Evaluation[/bold yellow]\n")

    for category, info in REVIEW_CHECKLIST.items():
        console.print(f"\n[bold]{info['icon']} {info['name']}[/bold]")

        if Confirm.ask(f"Evaluate {info['name']} checks?"):
            for check in info["checks"]:
                console.print(f"\n  [{check['severity']}] {check['check']}")
                status = Prompt.ask(
                    "  Status",
                    choices=["Pass", "Fail", "Partial", "N/A"],
                    default="N/A"
                )
                notes = ""
                if status in ["Fail", "Partial"]:
                    notes = Prompt.ask("  Notes", default="")

                    # Auto-create finding for failures
                    if status == "Fail" and check["severity"] in ["Critical", "High"]:
                        if Confirm.ask("  Create finding for this issue?"):
                            recommendation = Prompt.ask("  Recommendation")
                            component = Prompt.ask("  Affected component")
                            review.add_finding(
                                check["severity"],
                                f"Failed: {check['check']}",
                                notes,
                                component,
                                recommendation
                            )

                review.evaluate_check(category, check["id"], status, notes)

    # Additional findings
    console.print("\n[bold yellow]🔍 Additional Findings[/bold yellow]")

    while Confirm.ask("Add additional finding?"):
        severity = Prompt.ask("Severity", choices=["Critical", "High", "Medium", "Low"])
        title = Prompt.ask("Title")
        description = Prompt.ask("Description")
        component = Prompt.ask("Affected component")
        recommendation = Prompt.ask("Recommendation")
        review.add_finding(severity, title, description, component, recommendation)

    # Generate output
    console.print("\n[bold yellow]📄 Generating Review Report...[/bold yellow]\n")

    script_dir = Path(__file__).parent.parent.parent
    output_dir = script_dir / "reviews"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = system_name.lower().replace(" ", "-")

    # Save Markdown
    md_file = output_dir / f"{safe_name}-security-review-{timestamp}.md"
    with open(md_file, "w") as f:
        f.write(review.to_markdown())
    console.print(f"[green]✓[/green] Markdown saved: {md_file}")

    # Save JSON
    json_file = output_dir / f"{safe_name}-security-review-{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(review.to_dict(), f, indent=2)
    console.print(f"[green]✓[/green] JSON saved: {json_file}")

    # Display summary
    score = review.calculate_score()
    risk = review.get_risk_rating()

    summary_table = Table(title="Review Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="yellow")

    summary_table.add_row("Security Score", f"{score}%")
    summary_table.add_row("Risk Rating", risk)
    summary_table.add_row("Components Reviewed", str(len(review.components)))
    summary_table.add_row("Total Findings", str(len(review.findings)))
    summary_table.add_row("Critical Findings", str(len([f for f in review.findings if f["severity"] == "Critical"])))
    summary_table.add_row("High Findings", str(len([f for f in review.findings if f["severity"] == "High"])))

    console.print(summary_table)


@app.command()
def review(
    system: str = typer.Option(None, "--system", "-s", help="System name"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
):
    """Perform architecture security review"""
    if interactive or not system:
        interactive_review()
    else:
        console.print(f"[yellow]Reviewing: {system}[/yellow]")
        console.print("[yellow]Use --interactive for guided review[/yellow]")


@app.command()
def checklist():
    """Display security review checklist"""
    print_banner()

    for category, info in REVIEW_CHECKLIST.items():
        table = Table(title=f"{info['icon']} {info['name']}")
        table.add_column("ID", style="cyan")
        table.add_column("Check", style="white")
        table.add_column("Severity", style="yellow")

        for check in info["checks"]:
            severity_color = {
                "Critical": "red",
                "High": "orange1",
                "Medium": "yellow",
                "Low": "green"
            }.get(check["severity"], "white")

            table.add_row(
                check["id"],
                check["check"],
                f"[{severity_color}]{check['severity']}[/{severity_color}]"
            )

        console.print(table)
        console.print()


@app.command()
def template(
    output: str = typer.Option(".", "--output", "-o", help="Output directory"),
):
    """Generate review template"""
    template_content = """# Architecture Security Review Template

## System Information
- **System Name:**
- **Reviewer:**
- **Date:**

## Components
| Component | Type | Description |
|-----------|------|-------------|
| | | |

## Security Checklist

### Authentication
- [ ] MFA implemented
- [ ] Strong password policy
- [ ] Session management
- [ ] Credential storage

### Authorization
- [ ] RBAC/ABAC
- [ ] Least privilege
- [ ] API authorization

### Data Protection
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Key management

### Network Security
- [ ] Segmentation
- [ ] Firewall rules
- [ ] WAF/IDS

### Logging
- [ ] Centralized logging
- [ ] Security events
- [ ] Alerting

## Findings
| ID | Severity | Title | Component | Recommendation |
|----|----------|-------|-----------|----------------|
| | | | | |

## Recommendations
1.
2.
3.
"""
    output_path = Path(output) / "architecture-review-template.md"
    with open(output_path, "w") as f:
        f.write(template_content)
    console.print(f"[green]✓[/green] Template saved: {output_path}")


if __name__ == "__main__":
    app()
