#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Compliance Check Tool
Verifica el estado de compliance contra múltiples frameworks
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
except ImportError:
    print("Installing required packages...")
    os.system("pip install click rich pyyaml")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    NOT_ASSESSED = "not_assessed"

class Framework(Enum):
    ISO27001 = "ISO 27001:2022"
    SOC2 = "SOC 2 Type II"
    PCI_DSS = "PCI-DSS v4.0"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    NIST_CSF = "NIST CSF 2.0"

@dataclass
class Control:
    id: str
    name: str
    description: str
    framework: str
    category: str
    status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    evidence: List[str] = field(default_factory=list)
    last_assessed: Optional[str] = None
    owner: Optional[str] = None
    notes: str = ""

@dataclass
class ComplianceResult:
    framework: str
    total_controls: int
    compliant: int
    partial: int
    non_compliant: int
    not_applicable: int
    not_assessed: int
    score: float
    findings: List[Dict] = field(default_factory=list)

# ══════════════════════════════════════════════════════════════════════════════
# FRAMEWORK DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

FRAMEWORK_CONTROLS = {
    "ISO27001": {
        "A.5": {"name": "Organizational Controls", "count": 37},
        "A.6": {"name": "People Controls", "count": 8},
        "A.7": {"name": "Physical Controls", "count": 14},
        "A.8": {"name": "Technological Controls", "count": 34},
    },
    "SOC2": {
        "CC1": {"name": "Control Environment", "count": 5},
        "CC2": {"name": "Communication and Information", "count": 3},
        "CC3": {"name": "Risk Assessment", "count": 4},
        "CC4": {"name": "Monitoring Activities", "count": 2},
        "CC5": {"name": "Control Activities", "count": 3},
        "CC6": {"name": "Logical and Physical Access", "count": 8},
        "CC7": {"name": "System Operations", "count": 5},
        "CC8": {"name": "Change Management", "count": 1},
        "CC9": {"name": "Risk Mitigation", "count": 2},
    },
    "PCI-DSS": {
        "1": {"name": "Network Security Controls", "count": 12},
        "2": {"name": "Secure Configurations", "count": 8},
        "3": {"name": "Protect Account Data", "count": 15},
        "4": {"name": "Protect Cardholder Data", "count": 5},
        "5": {"name": "Protect Against Malware", "count": 8},
        "6": {"name": "Secure Systems and Software", "count": 12},
        "7": {"name": "Restrict Access", "count": 6},
        "8": {"name": "Identify and Authenticate", "count": 15},
        "9": {"name": "Restrict Physical Access", "count": 10},
        "10": {"name": "Log and Monitor", "count": 12},
        "11": {"name": "Test Security", "count": 10},
        "12": {"name": "Support Security Policies", "count": 15},
    },
    "GDPR": {
        "Art5": {"name": "Principles", "count": 7},
        "Art6": {"name": "Lawfulness", "count": 6},
        "Art7": {"name": "Consent", "count": 4},
        "Art12-23": {"name": "Data Subject Rights", "count": 12},
        "Art24-31": {"name": "Controller Obligations", "count": 8},
        "Art32-34": {"name": "Security", "count": 6},
        "Art35-36": {"name": "DPIA", "count": 4},
        "Art37-39": {"name": "DPO", "count": 3},
    },
    "HIPAA": {
        "Admin": {"name": "Administrative Safeguards", "count": 12},
        "Physical": {"name": "Physical Safeguards", "count": 6},
        "Technical": {"name": "Technical Safeguards", "count": 9},
        "Policies": {"name": "Policies and Procedures", "count": 4},
        "Documentation": {"name": "Documentation", "count": 3},
    },
    "NIST-CSF": {
        "GV": {"name": "Govern", "count": 6},
        "ID": {"name": "Identify", "count": 6},
        "PR": {"name": "Protect", "count": 5},
        "DE": {"name": "Detect", "count": 2},
        "RS": {"name": "Respond", "count": 4},
        "RC": {"name": "Recover", "count": 2},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# COMPLIANCE CHECKER CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ComplianceChecker:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.controls_path = self.workspace / "controls"
        self.compliance_path = self.workspace / "compliance"
        self.reports_path = self.workspace / "reports" / "compliance"
        self.controls: Dict[str, List[Control]] = {}
        
    def load_controls(self, framework: str) -> List[Control]:
        """Load controls from YAML files"""
        controls = []
        framework_path = self.controls_path / framework.lower()
        
        if framework_path.exists():
            for file in framework_path.glob("*.yaml"):
                try:
                    with open(file, 'r') as f:
                        data = yaml.safe_load(f)
                        if data:
                            for ctrl in data.get('controls', [data]):
                                control = Control(
                                    id=ctrl.get('id', ''),
                                    name=ctrl.get('name', ''),
                                    description=ctrl.get('description', ''),
                                    framework=framework,
                                    category=ctrl.get('category', ''),
                                    status=ComplianceStatus(ctrl.get('status', 'not_assessed')),
                                    evidence=ctrl.get('evidence', []),
                                    last_assessed=ctrl.get('last_assessed'),
                                    owner=ctrl.get('owner'),
                                    notes=ctrl.get('notes', '')
                                )
                                controls.append(control)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not load {file}: {e}[/yellow]")
        
        # If no controls loaded, create sample based on framework definition
        if not controls and framework in FRAMEWORK_CONTROLS:
            for domain, info in FRAMEWORK_CONTROLS[framework].items():
                for i in range(info['count']):
                    controls.append(Control(
                        id=f"{domain}.{i+1}",
                        name=f"{info['name']} Control {i+1}",
                        description=f"Control {i+1} for {info['name']}",
                        framework=framework,
                        category=domain,
                        status=ComplianceStatus.NOT_ASSESSED
                    ))
        
        self.controls[framework] = controls
        return controls
    
    def assess_compliance(self, framework: str) -> ComplianceResult:
        """Assess compliance for a specific framework"""
        controls = self.load_controls(framework)
        
        compliant = sum(1 for c in controls if c.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for c in controls if c.status == ComplianceStatus.PARTIAL)
        non_compliant = sum(1 for c in controls if c.status == ComplianceStatus.NON_COMPLIANT)
        not_applicable = sum(1 for c in controls if c.status == ComplianceStatus.NOT_APPLICABLE)
        not_assessed = sum(1 for c in controls if c.status == ComplianceStatus.NOT_ASSESSED)
        
        total = len(controls)
        assessed = total - not_assessed - not_applicable
        
        if assessed > 0:
            score = ((compliant + (partial * 0.5)) / assessed) * 100
        else:
            score = 0.0
        
        findings = [
            {
                "control_id": c.id,
                "control_name": c.name,
                "status": c.status.value,
                "notes": c.notes
            }
            for c in controls if c.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.PARTIAL]
        ]
        
        return ComplianceResult(
            framework=framework,
            total_controls=total,
            compliant=compliant,
            partial=partial,
            non_compliant=non_compliant,
            not_applicable=not_applicable,
            not_assessed=not_assessed,
            score=round(score, 2),
            findings=findings
        )
    
    def check_all_frameworks(self) -> Dict[str, ComplianceResult]:
        """Check compliance across all frameworks"""
        results = {}
        for framework in FRAMEWORK_CONTROLS.keys():
            results[framework] = self.assess_compliance(framework)
        return results
    
    def generate_report(self, results: Dict[str, ComplianceResult], format: str = "console") -> str:
        """Generate compliance report"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        if format == "console":
            return self._console_report(results)
        elif format == "json":
            return self._json_report(results, timestamp)
        elif format == "yaml":
            return self._yaml_report(results, timestamp)
        elif format == "markdown":
            return self._markdown_report(results, timestamp)
        else:
            return self._console_report(results)
    
    def _console_report(self, results: Dict[str, ComplianceResult]) -> str:
        """Generate console report"""
        console.print("\n")
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - COMPLIANCE REPORT[/bold white]",
            border_style="white"
        ))
        console.print(f"\n[dim]Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
        
        # Summary Table
        table = Table(title="Compliance Summary", show_header=True, header_style="bold cyan")
        table.add_column("Framework", style="white", width=20)
        table.add_column("Score", justify="center", width=10)
        table.add_column("Compliant", justify="center", style="green", width=10)
        table.add_column("Partial", justify="center", style="yellow", width=10)
        table.add_column("Non-Compliant", justify="center", style="red", width=12)
        table.add_column("N/A", justify="center", style="dim", width=8)
        table.add_column("Not Assessed", justify="center", style="blue", width=12)
        
        for framework, result in results.items():
            score_color = "green" if result.score >= 80 else "yellow" if result.score >= 60 else "red"
            table.add_row(
                framework,
                f"[{score_color}]{result.score}%[/{score_color}]",
                str(result.compliant),
                str(result.partial),
                str(result.non_compliant),
                str(result.not_applicable),
                str(result.not_assessed)
            )
        
        console.print(table)
        
        # Findings
        total_findings = sum(len(r.findings) for r in results.values())
        if total_findings > 0:
            console.print(f"\n[bold red]⚠ Total Findings: {total_findings}[/bold red]\n")
            
            findings_table = Table(title="Top Findings", show_header=True, header_style="bold red")
            findings_table.add_column("Framework", width=12)
            findings_table.add_column("Control ID", width=15)
            findings_table.add_column("Control Name", width=30)
            findings_table.add_column("Status", width=15)
            
            count = 0
            for framework, result in results.items():
                for finding in result.findings[:5]:  # Top 5 per framework
                    if count >= 20:  # Max 20 total
                        break
                    status_color = "red" if finding['status'] == 'non_compliant' else "yellow"
                    findings_table.add_row(
                        framework,
                        finding['control_id'],
                        finding['control_name'][:30],
                        f"[{status_color}]{finding['status']}[/{status_color}]"
                    )
                    count += 1
            
            console.print(findings_table)
        
        return "Report displayed"
    
    def _json_report(self, results: Dict[str, ComplianceResult], timestamp: str) -> str:
        """Generate JSON report"""
        report = {
            "report_type": "compliance_check",
            "generated": timestamp,
            "organization": os.getenv("ORG_NAME", "Organization"),
            "results": {}
        }
        
        for framework, result in results.items():
            report["results"][framework] = {
                "score": result.score,
                "total_controls": result.total_controls,
                "compliant": result.compliant,
                "partial": result.partial,
                "non_compliant": result.non_compliant,
                "not_applicable": result.not_applicable,
                "not_assessed": result.not_assessed,
                "findings": result.findings
            }
        
        # Save to file
        self.reports_path.mkdir(parents=True, exist_ok=True)
        report_file = self.reports_path / f"compliance_report_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        console.print(f"[green]Report saved to: {report_file}[/green]")
        return str(report_file)
    
    def _yaml_report(self, results: Dict[str, ComplianceResult], timestamp: str) -> str:
        """Generate YAML report"""
        report = {
            "report_type": "compliance_check",
            "generated": timestamp,
            "results": {}
        }
        
        for framework, result in results.items():
            report["results"][framework] = {
                "score": result.score,
                "total_controls": result.total_controls,
                "status_breakdown": {
                    "compliant": result.compliant,
                    "partial": result.partial,
                    "non_compliant": result.non_compliant,
                    "not_applicable": result.not_applicable,
                    "not_assessed": result.not_assessed
                },
                "findings_count": len(result.findings)
            }
        
        self.reports_path.mkdir(parents=True, exist_ok=True)
        report_file = self.reports_path / f"compliance_report_{timestamp}.yaml"
        with open(report_file, 'w') as f:
            yaml.dump(report, f, default_flow_style=False)
        
        console.print(f"[green]Report saved to: {report_file}[/green]")
        return str(report_file)
    
    def _markdown_report(self, results: Dict[str, ComplianceResult], timestamp: str) -> str:
        """Generate Markdown report"""
        lines = [
            "# ⚪ WHITE TEAM GRC - Compliance Report",
            "",
            f"**Generated:** {timestamp}",
            "",
            "## Summary",
            "",
            "| Framework | Score | Compliant | Partial | Non-Compliant | N/A | Not Assessed |",
            "|-----------|-------|-----------|---------|---------------|-----|--------------|"
        ]
        
        for framework, result in results.items():
            lines.append(
                f"| {framework} | {result.score}% | {result.compliant} | {result.partial} | "
                f"{result.non_compliant} | {result.not_applicable} | {result.not_assessed} |"
            )
        
        lines.extend(["", "## Findings", ""])
        
        for framework, result in results.items():
            if result.findings:
                lines.append(f"### {framework}")
                lines.append("")
                for finding in result.findings:
                    lines.append(f"- **{finding['control_id']}**: {finding['control_name']} - {finding['status']}")
                lines.append("")
        
        self.reports_path.mkdir(parents=True, exist_ok=True)
        report_file = self.reports_path / f"compliance_report_{timestamp}.md"
        with open(report_file, 'w') as f:
            f.write("\n".join(lines))
        
        console.print(f"[green]Report saved to: {report_file}[/green]")
        return str(report_file)

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--framework', '-f', type=click.Choice(['ISO27001', 'SOC2', 'PCI-DSS', 'GDPR', 'HIPAA', 'NIST-CSF', 'all']),
              default='all', help='Framework to check')
@click.option('--format', '-o', type=click.Choice(['console', 'json', 'yaml', 'markdown']),
              default='console', help='Output format')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.',
              help='Workspace path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Compliance Check')
def main(framework: str, format: str, workspace: str, verbose: bool):
    """
    ⚪ WHITE TEAM GRC - Compliance Check Tool
    
    Verifica el estado de compliance contra múltiples frameworks de seguridad.
    """
    checker = ComplianceChecker(workspace)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Checking compliance...", total=None)
        
        if framework == 'all':
            results = checker.check_all_frameworks()
        else:
            results = {framework: checker.assess_compliance(framework)}
        
        progress.update(task, completed=True)
    
    checker.generate_report(results, format)
    
    # Exit code based on compliance
    worst_score = min(r.score for r in results.values())
    if worst_score < 60:
        sys.exit(2)  # Critical
    elif worst_score < 80:
        sys.exit(1)  # Warning
    else:
        sys.exit(0)  # OK

if __name__ == '__main__':
    main()
