#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Gap Analysis Tool
Análisis de brechas de compliance contra frameworks
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn
    from rich import print as rprint
except ImportError:
    print("Installing required packages...")
    os.system("pip install click rich pyyaml")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn
    from rich import print as rprint

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

class ImplementationStatus(Enum):
    IMPLEMENTED = "implemented"
    PARTIAL = "partial"
    PLANNED = "planned"
    NOT_IMPLEMENTED = "not_implemented"
    NOT_APPLICABLE = "not_applicable"

class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ControlGap:
    control_id: str
    control_name: str
    domain: str
    current_status: ImplementationStatus
    target_status: ImplementationStatus
    gap_percentage: float
    priority: Priority
    effort_hours: int
    remediation_steps: List[str]
    dependencies: List[str] = field(default_factory=list)
    owner: str = ""
    due_date: str = ""

@dataclass
class DomainGap:
    domain_id: str
    domain_name: str
    total_controls: int
    implemented: int
    partial: int
    planned: int
    not_implemented: int
    not_applicable: int
    compliance_percentage: float
    gaps: List[ControlGap]

@dataclass
class GapAnalysisResult:
    framework: str
    analysis_date: str
    target_compliance: float
    current_compliance: float
    gap_percentage: float
    domains: List[DomainGap]
    total_gaps: int
    critical_gaps: int
    estimated_effort_hours: int
    remediation_roadmap: List[Dict]

# ══════════════════════════════════════════════════════════════════════════════
# FRAMEWORK REQUIREMENTS
# ══════════════════════════════════════════════════════════════════════════════

FRAMEWORK_REQUIREMENTS = {
    "ISO27001": {
        "name": "ISO 27001:2022",
        "domains": {
            "A.5": {
                "name": "Organizational Controls",
                "controls": [
                    {"id": "A.5.1", "name": "Policies for information security", "effort": 16, "priority": "high"},
                    {"id": "A.5.2", "name": "Information security roles", "effort": 8, "priority": "high"},
                    {"id": "A.5.3", "name": "Segregation of duties", "effort": 24, "priority": "medium"},
                    {"id": "A.5.4", "name": "Management responsibilities", "effort": 8, "priority": "high"},
                    {"id": "A.5.5", "name": "Contact with authorities", "effort": 4, "priority": "low"},
                    {"id": "A.5.6", "name": "Contact with special interest groups", "effort": 4, "priority": "low"},
                    {"id": "A.5.7", "name": "Threat intelligence", "effort": 40, "priority": "medium"},
                    {"id": "A.5.8", "name": "Information security in project management", "effort": 16, "priority": "medium"},
                    {"id": "A.5.9", "name": "Inventory of information assets", "effort": 40, "priority": "high"},
                    {"id": "A.5.10", "name": "Acceptable use of assets", "effort": 8, "priority": "medium"},
                ]
            },
            "A.6": {
                "name": "People Controls",
                "controls": [
                    {"id": "A.6.1", "name": "Screening", "effort": 16, "priority": "high"},
                    {"id": "A.6.2", "name": "Terms and conditions of employment", "effort": 8, "priority": "high"},
                    {"id": "A.6.3", "name": "Information security awareness", "effort": 40, "priority": "high"},
                    {"id": "A.6.4", "name": "Disciplinary process", "effort": 8, "priority": "medium"},
                    {"id": "A.6.5", "name": "Responsibilities after termination", "effort": 8, "priority": "high"},
                ]
            },
            "A.7": {
                "name": "Physical Controls",
                "controls": [
                    {"id": "A.7.1", "name": "Physical security perimeters", "effort": 80, "priority": "high"},
                    {"id": "A.7.2", "name": "Physical entry", "effort": 40, "priority": "high"},
                    {"id": "A.7.3", "name": "Securing offices and facilities", "effort": 24, "priority": "medium"},
                    {"id": "A.7.4", "name": "Physical security monitoring", "effort": 40, "priority": "medium"},
                ]
            },
            "A.8": {
                "name": "Technological Controls",
                "controls": [
                    {"id": "A.8.1", "name": "User endpoint devices", "effort": 40, "priority": "high"},
                    {"id": "A.8.2", "name": "Privileged access rights", "effort": 40, "priority": "critical"},
                    {"id": "A.8.3", "name": "Information access restriction", "effort": 24, "priority": "high"},
                    {"id": "A.8.4", "name": "Access to source code", "effort": 16, "priority": "medium"},
                    {"id": "A.8.5", "name": "Secure authentication", "effort": 40, "priority": "critical"},
                    {"id": "A.8.6", "name": "Capacity management", "effort": 16, "priority": "medium"},
                    {"id": "A.8.7", "name": "Protection against malware", "effort": 24, "priority": "critical"},
                    {"id": "A.8.8", "name": "Management of technical vulnerabilities", "effort": 40, "priority": "critical"},
                    {"id": "A.8.9", "name": "Configuration management", "effort": 40, "priority": "high"},
                    {"id": "A.8.10", "name": "Information deletion", "effort": 16, "priority": "medium"},
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
                    {"id": "CC1.1", "name": "Integrity and Ethical Values", "effort": 16, "priority": "high"},
                    {"id": "CC1.2", "name": "Board Independence", "effort": 8, "priority": "medium"},
                    {"id": "CC1.3", "name": "Management Structure", "effort": 8, "priority": "high"},
                    {"id": "CC1.4", "name": "Commitment to Competence", "effort": 16, "priority": "medium"},
                    {"id": "CC1.5", "name": "Accountability", "effort": 8, "priority": "high"},
                ]
            },
            "CC6": {
                "name": "Logical and Physical Access",
                "controls": [
                    {"id": "CC6.1", "name": "Logical Access Security", "effort": 40, "priority": "critical"},
                    {"id": "CC6.2", "name": "User Registration", "effort": 16, "priority": "high"},
                    {"id": "CC6.3", "name": "User Access Removal", "effort": 16, "priority": "high"},
                    {"id": "CC6.4", "name": "Access Review", "effort": 24, "priority": "high"},
                    {"id": "CC6.5", "name": "Physical Access", "effort": 40, "priority": "high"},
                    {"id": "CC6.6", "name": "Logical Access Restrictions", "effort": 40, "priority": "critical"},
                    {"id": "CC6.7", "name": "Data Transmission Protection", "effort": 24, "priority": "critical"},
                    {"id": "CC6.8", "name": "Malware Prevention", "effort": 24, "priority": "critical"},
                ]
            },
            "CC7": {
                "name": "System Operations",
                "controls": [
                    {"id": "CC7.1", "name": "Security Event Detection", "effort": 40, "priority": "critical"},
                    {"id": "CC7.2", "name": "Anomaly Monitoring", "effort": 40, "priority": "high"},
                    {"id": "CC7.3", "name": "Security Event Evaluation", "effort": 24, "priority": "high"},
                    {"id": "CC7.4", "name": "Incident Response", "effort": 40, "priority": "critical"},
                    {"id": "CC7.5", "name": "Recovery from Incidents", "effort": 40, "priority": "high"},
                ]
            }
        }
    },
    "PCI-DSS": {
        "name": "PCI-DSS v4.0",
        "domains": {
            "Req1": {
                "name": "Network Security Controls",
                "controls": [
                    {"id": "1.1", "name": "Network security controls defined", "effort": 24, "priority": "critical"},
                    {"id": "1.2", "name": "Network security controls configured", "effort": 40, "priority": "critical"},
                    {"id": "1.3", "name": "Network access to CDE restricted", "effort": 40, "priority": "critical"},
                    {"id": "1.4", "name": "Network connections controlled", "effort": 24, "priority": "critical"},
                ]
            },
            "Req8": {
                "name": "Identify and Authenticate",
                "controls": [
                    {"id": "8.1", "name": "User identification management", "effort": 24, "priority": "critical"},
                    {"id": "8.2", "name": "User authentication management", "effort": 24, "priority": "critical"},
                    {"id": "8.3", "name": "Strong authentication", "effort": 40, "priority": "critical"},
                    {"id": "8.4", "name": "MFA for CDE access", "effort": 40, "priority": "critical"},
                    {"id": "8.5", "name": "MFA configuration", "effort": 16, "priority": "high"},
                ]
            }
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# GAP ANALYZER CLASS
# ══════════════════════════════════════════════════════════════════════════════

class GapAnalyzer:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.controls_path = self.workspace / "controls"
        self.reports_path = self.workspace / "reports" / "compliance"
        self.current_state: Dict[str, ImplementationStatus] = {}
        
    def load_current_state(self, framework: str) -> Dict[str, ImplementationStatus]:
        """Load current implementation state from controls directory"""
        self.current_state = {}
        framework_path = self.controls_path / framework.lower()
        
        if framework_path.exists():
            for file in framework_path.glob("*.yaml"):
                try:
                    with open(file, 'r') as f:
                        data = yaml.safe_load(f)
                        if data:
                            for ctrl in data.get('controls', [data]):
                                ctrl_id = ctrl.get('id', '')
                                status = ctrl.get('status', 'not_implemented')
                                self.current_state[ctrl_id] = ImplementationStatus(status)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not load {file}: {e}[/yellow]")
        
        return self.current_state
    
    def analyze_gaps(self, framework: str, target: float = 100.0) -> GapAnalysisResult:
        """Perform gap analysis for a framework"""
        if framework not in FRAMEWORK_REQUIREMENTS:
            console.print(f"[red]Unknown framework: {framework}[/red]")
            return None
        
        fw_data = FRAMEWORK_REQUIREMENTS[framework]
        self.load_current_state(framework)
        
        console.print(Panel.fit(
            f"[bold white]⚪ GAP ANALYSIS: {fw_data['name']}[/bold white]",
            border_style="white"
        ))
        
        domains = []
        total_gaps = 0
        critical_gaps = 0
        total_effort = 0
        all_gaps = []
        
        for domain_id, domain_data in fw_data["domains"].items():
            domain_gaps = []
            implemented = 0
            partial = 0
            planned = 0
            not_implemented = 0
            not_applicable = 0
            
            for control in domain_data["controls"]:
                ctrl_id = control["id"]
                status = self.current_state.get(ctrl_id, ImplementationStatus.NOT_IMPLEMENTED)
                
                if status == ImplementationStatus.IMPLEMENTED:
                    implemented += 1
                elif status == ImplementationStatus.PARTIAL:
                    partial += 1
                    gap = self._create_gap(control, domain_data["name"], status, 50)
                    domain_gaps.append(gap)
                    all_gaps.append(gap)
                    total_effort += gap.effort_hours // 2
                elif status == ImplementationStatus.PLANNED:
                    planned += 1
                    gap = self._create_gap(control, domain_data["name"], status, 100)
                    domain_gaps.append(gap)
                    all_gaps.append(gap)
                    total_effort += gap.effort_hours
                elif status == ImplementationStatus.NOT_APPLICABLE:
                    not_applicable += 1
                else:
                    not_implemented += 1
                    gap = self._create_gap(control, domain_data["name"], status, 100)
                    domain_gaps.append(gap)
                    all_gaps.append(gap)
                    total_effort += gap.effort_hours
                    if gap.priority == Priority.CRITICAL:
                        critical_gaps += 1
            
            total = len(domain_data["controls"])
            applicable = total - not_applicable
            if applicable > 0:
                compliance = ((implemented + partial * 0.5) / applicable) * 100
            else:
                compliance = 100.0
            
            total_gaps += len(domain_gaps)
            
            domains.append(DomainGap(
                domain_id=domain_id,
                domain_name=domain_data["name"],
                total_controls=total,
                implemented=implemented,
                partial=partial,
                planned=planned,
                not_implemented=not_implemented,
                not_applicable=not_applicable,
                compliance_percentage=round(compliance, 2),
                gaps=domain_gaps
            ))
        
        # Calculate overall compliance
        total_controls = sum(d.total_controls for d in domains)
        total_applicable = sum(d.total_controls - d.not_applicable for d in domains)
        total_implemented = sum(d.implemented + d.partial * 0.5 for d in domains)
        
        if total_applicable > 0:
            current_compliance = (total_implemented / total_applicable) * 100
        else:
            current_compliance = 100.0
        
        gap_percentage = target - current_compliance
        
        # Generate remediation roadmap
        roadmap = self._generate_roadmap(all_gaps)
        
        return GapAnalysisResult(
            framework=framework,
            analysis_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            target_compliance=target,
            current_compliance=round(current_compliance, 2),
            gap_percentage=round(max(0, gap_percentage), 2),
            domains=domains,
            total_gaps=total_gaps,
            critical_gaps=critical_gaps,
            estimated_effort_hours=total_effort,
            remediation_roadmap=roadmap
        )
    
    def _create_gap(self, control: Dict, domain_name: str, 
                    status: ImplementationStatus, gap_pct: float) -> ControlGap:
        """Create a control gap entry"""
        priority = Priority(control.get("priority", "medium"))
        
        remediation_steps = [
            f"Assess current state of {control['name']}",
            "Identify required resources and dependencies",
            "Develop implementation plan",
            "Implement control",
            "Test and validate implementation",
            "Document evidence and procedures"
        ]
        
        return ControlGap(
            control_id=control["id"],
            control_name=control["name"],
            domain=domain_name,
            current_status=status,
            target_status=ImplementationStatus.IMPLEMENTED,
            gap_percentage=gap_pct,
            priority=priority,
            effort_hours=control.get("effort", 16),
            remediation_steps=remediation_steps
        )
    
    def _generate_roadmap(self, gaps: List[ControlGap]) -> List[Dict]:
        """Generate remediation roadmap"""
        # Sort by priority
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        
        sorted_gaps = sorted(gaps, key=lambda g: priority_order[g.priority])
        
        roadmap = []
        current_phase = 1
        current_effort = 0
        phase_items = []
        
        for gap in sorted_gaps:
            if current_effort + gap.effort_hours > 160:  # ~1 month
                roadmap.append({
                    "phase": current_phase,
                    "estimated_hours": current_effort,
                    "items": phase_items
                })
                current_phase += 1
                current_effort = 0
                phase_items = []
            
            phase_items.append({
                "control_id": gap.control_id,
                "control_name": gap.control_name,
                "priority": gap.priority.value,
                "effort_hours": gap.effort_hours
            })
            current_effort += gap.effort_hours
        
        if phase_items:
            roadmap.append({
                "phase": current_phase,
                "estimated_hours": current_effort,
                "items": phase_items
            })
        
        return roadmap
    
    def display_results(self, result: GapAnalysisResult) -> None:
        """Display gap analysis results"""
        # Summary panel
        compliance_color = "green" if result.current_compliance >= 80 else "yellow" if result.current_compliance >= 60 else "red"
        
        console.print(f"\n[bold]Analysis Date:[/bold] {result.analysis_date}")
        console.print(f"[bold]Target Compliance:[/bold] {result.target_compliance}%")
        console.print(f"[bold]Current Compliance:[/bold] [{compliance_color}]{result.current_compliance}%[/{compliance_color}]")
        console.print(f"[bold]Gap:[/bold] [red]{result.gap_percentage}%[/red]")
        console.print(f"[bold]Total Gaps:[/bold] {result.total_gaps}")
        console.print(f"[bold]Critical Gaps:[/bold] [red]{result.critical_gaps}[/red]")
        console.print(f"[bold]Estimated Effort:[/bold] {result.estimated_effort_hours} hours (~{result.estimated_effort_hours // 40} weeks)")
        
        # Domain breakdown
        console.print("\n[bold cyan]Domain Breakdown:[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Domain", width=30)
        table.add_column("Compliance", justify="center", width=12)
        table.add_column("Impl", justify="center", width=6)
        table.add_column("Partial", justify="center", width=8)
        table.add_column("Planned", justify="center", width=8)
        table.add_column("Missing", justify="center", width=8)
        table.add_column("Gaps", justify="center", width=6)
        
        for domain in result.domains:
            comp_color = "green" if domain.compliance_percentage >= 80 else "yellow" if domain.compliance_percentage >= 60 else "red"
            table.add_row(
                f"{domain.domain_id}: {domain.domain_name}"[:30],
                f"[{comp_color}]{domain.compliance_percentage}%[/{comp_color}]",
                str(domain.implemented),
                str(domain.partial),
                str(domain.planned),
                str(domain.not_implemented),
                str(len(domain.gaps))
            )
        
        console.print(table)
        
        # Top gaps
        all_gaps = []
        for domain in result.domains:
            all_gaps.extend(domain.gaps)
        
        if all_gaps:
            console.print("\n[bold red]Top Priority Gaps:[/bold red]\n")
            
            gaps_table = Table(show_header=True, header_style="bold red")
            gaps_table.add_column("Control", width=12)
            gaps_table.add_column("Name", width=35)
            gaps_table.add_column("Priority", width=10)
            gaps_table.add_column("Effort", width=10)
            gaps_table.add_column("Status", width=15)
            
            priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
            sorted_gaps = sorted(all_gaps, key=lambda g: priority_order[g.priority])[:10]
            
            priority_colors = {
                Priority.CRITICAL: "red",
                Priority.HIGH: "orange1",
                Priority.MEDIUM: "yellow",
                Priority.LOW: "green"
            }
            
            for gap in sorted_gaps:
                color = priority_colors[gap.priority]
                gaps_table.add_row(
                    gap.control_id,
                    gap.control_name[:35],
                    f"[{color}]{gap.priority.value.upper()}[/{color}]",
                    f"{gap.effort_hours}h",
                    gap.current_status.value
                )
            
            console.print(gaps_table)
        
        # Roadmap summary
        if result.remediation_roadmap:
            console.print("\n[bold cyan]Remediation Roadmap:[/bold cyan]\n")
            
            for phase in result.remediation_roadmap[:3]:  # Show first 3 phases
                console.print(f"[bold]Phase {phase['phase']}[/bold] (~{phase['estimated_hours']}h)")
                for item in phase['items'][:5]:
                    console.print(f"  • {item['control_id']}: {item['control_name']} [{item['priority']}]")
                if len(phase['items']) > 5:
                    console.print(f"  ... and {len(phase['items']) - 5} more")
                console.print()
    
    def save_results(self, result: GapAnalysisResult, format: str = "yaml") -> str:
        """Save gap analysis results"""
        self.reports_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result_dict = {
            "framework": result.framework,
            "analysis_date": result.analysis_date,
            "target_compliance": result.target_compliance,
            "current_compliance": result.current_compliance,
            "gap_percentage": result.gap_percentage,
            "total_gaps": result.total_gaps,
            "critical_gaps": result.critical_gaps,
            "estimated_effort_hours": result.estimated_effort_hours,
            "domains": [
                {
                    "domain_id": d.domain_id,
                    "domain_name": d.domain_name,
                    "compliance_percentage": d.compliance_percentage,
                    "total_controls": d.total_controls,
                    "implemented": d.implemented,
                    "partial": d.partial,
                    "planned": d.planned,
                    "not_implemented": d.not_implemented,
                    "gaps_count": len(d.gaps)
                }
                for d in result.domains
            ],
            "remediation_roadmap": result.remediation_roadmap
        }
        
        if format == "yaml":
            filepath = self.reports_path / f"gap_analysis_{result.framework}_{timestamp}.yaml"
            with open(filepath, 'w') as f:
                yaml.dump(result_dict, f, default_flow_style=False)
        else:
            filepath = self.reports_path / f"gap_analysis_{result.framework}_{timestamp}.json"
            with open(filepath, 'w') as f:
                json.dump(result_dict, f, indent=2)
        
        console.print(f"\n[green]✓ Results saved to: {filepath}[/green]")
        return str(filepath)

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--framework', '-f', type=click.Choice(['ISO27001', 'SOC2', 'PCI-DSS']),
              required=True, help='Framework to analyze')
@click.option('--target', '-t', type=float, default=100.0, help='Target compliance percentage')
@click.option('--format', '-o', type=click.Choice(['yaml', 'json']), default='yaml', help='Output format')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.', help='Workspace path')
@click.option('--save/--no-save', default=True, help='Save results to file')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Gap Analysis')
def main(framework: str, target: float, format: str, workspace: str, save: bool):
    """
    ⚪ WHITE TEAM GRC - Gap Analysis Tool
    
    Analiza brechas de compliance contra frameworks de seguridad.
    """
    analyzer = GapAnalyzer(workspace)
    
    result = analyzer.analyze_gaps(framework, target)
    
    if result:
        analyzer.display_results(result)
        if save:
            analyzer.save_results(result, format)

if __name__ == '__main__':
    main()
