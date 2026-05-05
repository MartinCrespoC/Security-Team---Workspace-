#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Audit Checklist Generator
Genera checklists de auditoría para múltiples frameworks
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
except ImportError:
    print("Installing required packages...")
    os.system("pip install click rich pyyaml")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# FRAMEWORK AUDIT REQUIREMENTS
# ══════════════════════════════════════════════════════════════════════════════

AUDIT_FRAMEWORKS = {
    "ISO27001": {
        "name": "ISO 27001:2022",
        "domains": {
            "A.5": {
                "name": "Organizational Controls",
                "controls": [
                    {"id": "A.5.1", "name": "Policies for information security", "evidence": ["Information security policy", "Policy review records"]},
                    {"id": "A.5.2", "name": "Information security roles and responsibilities", "evidence": ["RACI matrix", "Job descriptions"]},
                    {"id": "A.5.3", "name": "Segregation of duties", "evidence": ["Access matrix", "Role definitions"]},
                    {"id": "A.5.4", "name": "Management responsibilities", "evidence": ["Management commitment letter", "Meeting minutes"]},
                    {"id": "A.5.5", "name": "Contact with authorities", "evidence": ["Contact list", "Communication records"]},
                    {"id": "A.5.6", "name": "Contact with special interest groups", "evidence": ["Membership records", "Participation evidence"]},
                    {"id": "A.5.7", "name": "Threat intelligence", "evidence": ["Threat reports", "Intelligence feeds"]},
                    {"id": "A.5.8", "name": "Information security in project management", "evidence": ["Project security plans", "Risk assessments"]},
                    {"id": "A.5.9", "name": "Inventory of information and other associated assets", "evidence": ["Asset inventory", "Classification records"]},
                    {"id": "A.5.10", "name": "Acceptable use of information and other associated assets", "evidence": ["AUP policy", "Acknowledgment records"]},
                ]
            },
            "A.6": {
                "name": "People Controls",
                "controls": [
                    {"id": "A.6.1", "name": "Screening", "evidence": ["Background check records", "Verification procedures"]},
                    {"id": "A.6.2", "name": "Terms and conditions of employment", "evidence": ["Employment contracts", "NDA records"]},
                    {"id": "A.6.3", "name": "Information security awareness, education and training", "evidence": ["Training records", "Awareness materials"]},
                    {"id": "A.6.4", "name": "Disciplinary process", "evidence": ["Disciplinary policy", "Incident records"]},
                    {"id": "A.6.5", "name": "Responsibilities after termination or change of employment", "evidence": ["Exit procedures", "Access revocation records"]},
                ]
            },
            "A.7": {
                "name": "Physical Controls",
                "controls": [
                    {"id": "A.7.1", "name": "Physical security perimeters", "evidence": ["Facility diagrams", "Access control systems"]},
                    {"id": "A.7.2", "name": "Physical entry", "evidence": ["Access logs", "Visitor records"]},
                    {"id": "A.7.3", "name": "Securing offices, rooms and facilities", "evidence": ["Security assessments", "Lock records"]},
                    {"id": "A.7.4", "name": "Physical security monitoring", "evidence": ["CCTV records", "Monitoring logs"]},
                ]
            },
            "A.8": {
                "name": "Technological Controls",
                "controls": [
                    {"id": "A.8.1", "name": "User endpoint devices", "evidence": ["Device inventory", "MDM configuration"]},
                    {"id": "A.8.2", "name": "Privileged access rights", "evidence": ["PAM records", "Access reviews"]},
                    {"id": "A.8.3", "name": "Information access restriction", "evidence": ["Access control lists", "Permission matrices"]},
                    {"id": "A.8.4", "name": "Access to source code", "evidence": ["Repository access logs", "Code review records"]},
                    {"id": "A.8.5", "name": "Secure authentication", "evidence": ["MFA configuration", "Authentication logs"]},
                ]
            }
        }
    },
    "SOC2": {
        "name": "SOC 2 Type II",
        "domains": {
            "CC1": {
                "name": "Control Environment",
                "controls": [
                    {"id": "CC1.1", "name": "COSO Principle 1: Integrity and Ethical Values", "evidence": ["Code of conduct", "Ethics training records"]},
                    {"id": "CC1.2", "name": "COSO Principle 2: Board Independence", "evidence": ["Board charter", "Meeting minutes"]},
                    {"id": "CC1.3", "name": "COSO Principle 3: Management Structure", "evidence": ["Org chart", "Role descriptions"]},
                    {"id": "CC1.4", "name": "COSO Principle 4: Commitment to Competence", "evidence": ["Job descriptions", "Performance reviews"]},
                    {"id": "CC1.5", "name": "COSO Principle 5: Accountability", "evidence": ["Performance metrics", "Accountability matrix"]},
                ]
            },
            "CC6": {
                "name": "Logical and Physical Access Controls",
                "controls": [
                    {"id": "CC6.1", "name": "Logical Access Security Software", "evidence": ["Access control configuration", "User provisioning records"]},
                    {"id": "CC6.2", "name": "New User Registration", "evidence": ["Onboarding procedures", "Access request forms"]},
                    {"id": "CC6.3", "name": "User Access Removal", "evidence": ["Offboarding procedures", "Access revocation logs"]},
                    {"id": "CC6.4", "name": "Access Review", "evidence": ["Access review reports", "Recertification records"]},
                    {"id": "CC6.5", "name": "Physical Access Restrictions", "evidence": ["Badge access logs", "Facility access records"]},
                    {"id": "CC6.6", "name": "Logical Access Restrictions", "evidence": ["Firewall rules", "Network segmentation"]},
                    {"id": "CC6.7", "name": "Data Transmission Protection", "evidence": ["Encryption configuration", "TLS certificates"]},
                    {"id": "CC6.8", "name": "Malware Prevention", "evidence": ["Antivirus logs", "Malware scan reports"]},
                ]
            },
            "CC7": {
                "name": "System Operations",
                "controls": [
                    {"id": "CC7.1", "name": "Detection of Security Events", "evidence": ["SIEM configuration", "Alert logs"]},
                    {"id": "CC7.2", "name": "Monitoring for Anomalies", "evidence": ["Monitoring dashboards", "Anomaly reports"]},
                    {"id": "CC7.3", "name": "Security Event Evaluation", "evidence": ["Incident triage procedures", "Event analysis records"]},
                    {"id": "CC7.4", "name": "Incident Response", "evidence": ["IR plan", "Incident reports"]},
                    {"id": "CC7.5", "name": "Recovery from Incidents", "evidence": ["Recovery procedures", "Post-incident reviews"]},
                ]
            }
        }
    },
    "PCI-DSS": {
        "name": "PCI-DSS v4.0",
        "domains": {
            "1": {
                "name": "Network Security Controls",
                "controls": [
                    {"id": "1.1", "name": "Network security controls defined and understood", "evidence": ["Network diagrams", "Security policies"]},
                    {"id": "1.2", "name": "Network security controls configured and maintained", "evidence": ["Firewall configs", "Change records"]},
                    {"id": "1.3", "name": "Network access to CDE is restricted", "evidence": ["ACLs", "Segmentation tests"]},
                    {"id": "1.4", "name": "Network connections between trusted and untrusted networks controlled", "evidence": ["DMZ configuration", "Traffic logs"]},
                ]
            },
            "8": {
                "name": "Identify Users and Authenticate Access",
                "controls": [
                    {"id": "8.1", "name": "User identification management", "evidence": ["User ID policies", "Account management procedures"]},
                    {"id": "8.2", "name": "User authentication management", "evidence": ["Authentication policies", "Password configuration"]},
                    {"id": "8.3", "name": "Strong authentication for users and administrators", "evidence": ["MFA configuration", "Authentication logs"]},
                    {"id": "8.4", "name": "MFA for all access into CDE", "evidence": ["MFA enrollment records", "Access logs"]},
                    {"id": "8.5", "name": "MFA systems configured properly", "evidence": ["MFA configuration", "Testing records"]},
                ]
            }
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ChecklistItem:
    control_id: str
    control_name: str
    evidence_required: List[str]
    status: str = "not_tested"  # not_tested, pass, fail, partial, n/a
    findings: str = ""
    evidence_collected: List[str] = field(default_factory=list)
    tester: str = ""
    test_date: str = ""

@dataclass
class AuditChecklist:
    id: str
    framework: str
    scope: str
    audit_type: str
    start_date: str
    end_date: str
    lead_auditor: str
    team: List[str]
    items: List[ChecklistItem]
    status: str = "draft"

# ══════════════════════════════════════════════════════════════════════════════
# CHECKLIST GENERATOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ChecklistGenerator:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.audits_path = self.workspace / "audits"
        self.checklists_path = self.audits_path / "checklists"
        
    def list_frameworks(self) -> None:
        """List available frameworks for audit"""
        console.print(Panel.fit(
            "[bold white]⚪ AVAILABLE AUDIT FRAMEWORKS[/bold white]",
            border_style="white"
        ))
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Framework", width=15)
        table.add_column("Name", width=25)
        table.add_column("Domains", width=10)
        table.add_column("Controls", width=10)
        
        for fw_id, fw_data in AUDIT_FRAMEWORKS.items():
            total_controls = sum(
                len(domain["controls"]) 
                for domain in fw_data["domains"].values()
            )
            table.add_row(
                fw_id,
                fw_data["name"],
                str(len(fw_data["domains"])),
                str(total_controls)
            )
        
        console.print(table)
    
    def generate_checklist(self, framework: str, scope: str = "full", 
                          interactive: bool = True) -> AuditChecklist:
        """Generate audit checklist for a framework"""
        if framework not in AUDIT_FRAMEWORKS:
            console.print(f"[red]Unknown framework: {framework}[/red]")
            self.list_frameworks()
            return None
        
        fw_data = AUDIT_FRAMEWORKS[framework]
        
        console.print(Panel.fit(
            f"[bold white]⚪ GENERATING AUDIT CHECKLIST: {fw_data['name']}[/bold white]",
            border_style="white"
        ))
        
        if interactive:
            audit_info = self._get_audit_info()
        else:
            audit_info = self._default_audit_info()
        
        # Generate checklist items
        items = []
        domains_to_include = fw_data["domains"]
        
        if scope != "full":
            # Filter domains based on scope
            domains_to_include = {
                k: v for k, v in fw_data["domains"].items()
                if scope.lower() in k.lower() or scope.lower() in v["name"].lower()
            }
        
        for domain_id, domain_data in domains_to_include.items():
            console.print(f"[cyan]Adding domain: {domain_id} - {domain_data['name']}[/cyan]")
            for control in domain_data["controls"]:
                items.append(ChecklistItem(
                    control_id=control["id"],
                    control_name=control["name"],
                    evidence_required=control["evidence"]
                ))
        
        audit_id = f"AUD-{datetime.now().year}-{datetime.now().strftime('%m%d%H%M')}"
        
        checklist = AuditChecklist(
            id=audit_id,
            framework=framework,
            scope=scope,
            audit_type=audit_info["audit_type"],
            start_date=audit_info["start_date"],
            end_date=audit_info["end_date"],
            lead_auditor=audit_info["lead_auditor"],
            team=audit_info["team"],
            items=items
        )
        
        return checklist
    
    def _get_audit_info(self) -> Dict:
        """Get audit information interactively"""
        console.print("\n[cyan]Audit Information[/cyan]\n")
        
        audit_type = Prompt.ask(
            "Audit Type",
            choices=["internal", "external", "compliance", "follow-up"],
            default="internal"
        )
        
        lead_auditor = Prompt.ask("Lead Auditor")
        
        team = []
        console.print("\nEnter team members (empty to finish):")
        while True:
            member = Prompt.ask("Team Member", default="")
            if not member:
                break
            team.append(member)
        
        start_date = Prompt.ask("Start Date (YYYY-MM-DD)", 
                               default=datetime.now().strftime("%Y-%m-%d"))
        end_date = Prompt.ask("End Date (YYYY-MM-DD)",
                             default=(datetime.now().replace(day=datetime.now().day + 14)).strftime("%Y-%m-%d"))
        
        return {
            "audit_type": audit_type,
            "lead_auditor": lead_auditor,
            "team": team,
            "start_date": start_date,
            "end_date": end_date
        }
    
    def _default_audit_info(self) -> Dict:
        """Get default audit information"""
        return {
            "audit_type": "internal",
            "lead_auditor": "Auditor",
            "team": [],
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now().replace(day=datetime.now().day + 14)).strftime("%Y-%m-%d")
        }
    
    def save_checklist(self, checklist: AuditChecklist, format: str = "yaml") -> str:
        """Save checklist to file"""
        self.checklists_path.mkdir(parents=True, exist_ok=True)
        
        checklist_dict = {
            "id": checklist.id,
            "framework": checklist.framework,
            "scope": checklist.scope,
            "audit_type": checklist.audit_type,
            "start_date": checklist.start_date,
            "end_date": checklist.end_date,
            "lead_auditor": checklist.lead_auditor,
            "team": checklist.team,
            "status": checklist.status,
            "items": [
                {
                    "control_id": item.control_id,
                    "control_name": item.control_name,
                    "evidence_required": item.evidence_required,
                    "status": item.status,
                    "findings": item.findings,
                    "evidence_collected": item.evidence_collected,
                    "tester": item.tester,
                    "test_date": item.test_date
                }
                for item in checklist.items
            ],
            "summary": {
                "total_controls": len(checklist.items),
                "tested": 0,
                "passed": 0,
                "failed": 0,
                "partial": 0,
                "not_applicable": 0
            }
        }
        
        if format == "yaml":
            filepath = self.checklists_path / f"{checklist.id}.yaml"
            with open(filepath, 'w') as f:
                yaml.dump(checklist_dict, f, default_flow_style=False, allow_unicode=True)
        elif format == "json":
            filepath = self.checklists_path / f"{checklist.id}.json"
            with open(filepath, 'w') as f:
                json.dump(checklist_dict, f, indent=2)
        elif format == "markdown":
            filepath = self.checklists_path / f"{checklist.id}.md"
            content = self._generate_markdown(checklist)
            with open(filepath, 'w') as f:
                f.write(content)
        
        console.print(f"\n[green]✓ Checklist saved to: {filepath}[/green]")
        return str(filepath)
    
    def _generate_markdown(self, checklist: AuditChecklist) -> str:
        """Generate markdown format checklist"""
        lines = [
            f"# Audit Checklist: {checklist.id}",
            "",
            f"**Framework:** {checklist.framework}",
            f"**Scope:** {checklist.scope}",
            f"**Type:** {checklist.audit_type}",
            f"**Period:** {checklist.start_date} to {checklist.end_date}",
            f"**Lead Auditor:** {checklist.lead_auditor}",
            f"**Team:** {', '.join(checklist.team) if checklist.team else 'TBD'}",
            "",
            "---",
            "",
            "## Checklist Items",
            "",
            "| # | Control ID | Control Name | Status | Evidence Required |",
            "|---|------------|--------------|--------|-------------------|"
        ]
        
        for i, item in enumerate(checklist.items, 1):
            evidence = ", ".join(item.evidence_required[:2])
            if len(item.evidence_required) > 2:
                evidence += "..."
            lines.append(
                f"| {i} | {item.control_id} | {item.control_name} | ⬜ | {evidence} |"
            )
        
        lines.extend([
            "",
            "---",
            "",
            "## Status Legend",
            "",
            "- ⬜ Not Tested",
            "- ✅ Pass",
            "- ❌ Fail",
            "- ⚠️ Partial",
            "- ➖ N/A",
            "",
            "---",
            "",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        ])
        
        return "\n".join(lines)
    
    def display_checklist(self, checklist: AuditChecklist) -> None:
        """Display checklist summary"""
        console.print(Panel.fit(
            f"[bold white]⚪ AUDIT CHECKLIST: {checklist.id}[/bold white]",
            border_style="white"
        ))
        
        # Info table
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Field", style="cyan", width=15)
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Framework", checklist.framework)
        info_table.add_row("Scope", checklist.scope)
        info_table.add_row("Type", checklist.audit_type)
        info_table.add_row("Period", f"{checklist.start_date} to {checklist.end_date}")
        info_table.add_row("Lead Auditor", checklist.lead_auditor)
        info_table.add_row("Team", ", ".join(checklist.team) if checklist.team else "TBD")
        info_table.add_row("Total Controls", str(len(checklist.items)))
        
        console.print(info_table)
        
        # Controls table
        console.print("\n[bold]Controls to Test:[/bold]\n")
        
        controls_table = Table(show_header=True, header_style="bold cyan")
        controls_table.add_column("#", width=4)
        controls_table.add_column("Control ID", width=12)
        controls_table.add_column("Control Name", width=40)
        controls_table.add_column("Evidence", width=30)
        
        for i, item in enumerate(checklist.items[:20], 1):  # Show first 20
            evidence = ", ".join(item.evidence_required[:2])
            if len(item.evidence_required) > 2:
                evidence += "..."
            controls_table.add_row(
                str(i),
                item.control_id,
                item.control_name[:40],
                evidence[:30]
            )
        
        console.print(controls_table)
        
        if len(checklist.items) > 20:
            console.print(f"\n[dim]... and {len(checklist.items) - 20} more controls[/dim]")

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--framework', '-f', type=str, help='Framework to audit (ISO27001, SOC2, PCI-DSS)')
@click.option('--scope', '-s', type=str, default='full', help='Audit scope (full or specific domain)')
@click.option('--format', '-o', type=click.Choice(['yaml', 'json', 'markdown']), default='yaml', help='Output format')
@click.option('--list', '-l', 'list_fw', is_flag=True, help='List available frameworks')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.', help='Workspace path')
@click.option('--interactive/--no-interactive', '-i', default=True, help='Interactive mode')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Audit Checklist')
def main(framework: str, scope: str, format: str, list_fw: bool, workspace: str, interactive: bool):
    """
    ⚪ WHITE TEAM GRC - Audit Checklist Generator
    
    Genera checklists de auditoría para múltiples frameworks de compliance.
    """
    generator = ChecklistGenerator(workspace)
    
    if list_fw:
        generator.list_frameworks()
    elif framework:
        checklist = generator.generate_checklist(framework, scope, interactive)
        if checklist:
            generator.display_checklist(checklist)
            generator.save_checklist(checklist, format)
    else:
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - Audit Checklist Generator[/bold white]",
            border_style="white"
        ))
        generator.list_frameworks()
        console.print("\n[cyan]Usage:[/cyan]")
        console.print("  --framework FW   Generate checklist for framework")
        console.print("  --scope SCOPE    Limit to specific domain")
        console.print("  --format FORMAT  Output format (yaml, json, markdown)")
        console.print("  --list           List available frameworks")
        console.print("\n[dim]Example: python audit_checklist.py --framework ISO27001 --scope A.8[/dim]")

if __name__ == '__main__':
    main()
