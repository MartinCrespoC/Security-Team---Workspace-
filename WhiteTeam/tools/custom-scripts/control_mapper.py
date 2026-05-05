#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Control Mapper Tool
Mapea controles entre múltiples frameworks de compliance
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.tree import Tree
except ImportError:
    print("Installing required packages...")
    os.system("pip install click rich pyyaml")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.tree import Tree

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# CONTROL MAPPINGS DATABASE
# ══════════════════════════════════════════════════════════════════════════════

CONTROL_MAPPINGS = {
    # Access Control
    "access_control": {
        "name": "Access Control",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.5.15", "A.5.16", "A.5.17", "A.5.18", "A.8.2", "A.8.3"],
            "SOC2": ["CC6.1", "CC6.2", "CC6.3", "CC6.4"],
            "PCI_DSS": ["7.1", "7.2", "7.3", "8.1", "8.2", "8.3"],
            "NIST_CSF": ["PR.AC-1", "PR.AC-3", "PR.AC-4", "PR.AC-5"],
            "HIPAA": ["164.312(a)(1)", "164.312(d)"],
            "GDPR": ["Art.32"]
        }
    },
    "mfa": {
        "name": "Multi-Factor Authentication",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.8.5"],
            "SOC2": ["CC6.1"],
            "PCI_DSS": ["8.4", "8.4.2", "8.4.3"],
            "NIST_CSF": ["PR.AC-7"],
            "HIPAA": ["164.312(d)"],
            "GDPR": ["Art.32"]
        }
    },
    "encryption_at_rest": {
        "name": "Encryption at Rest",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.8.24"],
            "SOC2": ["CC6.1", "CC6.7"],
            "PCI_DSS": ["3.4", "3.5"],
            "NIST_CSF": ["PR.DS-1", "PR.DS-5"],
            "HIPAA": ["164.312(a)(2)(iv)"],
            "GDPR": ["Art.32"]
        }
    },
    "encryption_in_transit": {
        "name": "Encryption in Transit",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.8.24"],
            "SOC2": ["CC6.7"],
            "PCI_DSS": ["4.1", "4.2"],
            "NIST_CSF": ["PR.DS-2", "PR.DS-5"],
            "HIPAA": ["164.312(e)(1)", "164.312(e)(2)(ii)"],
            "GDPR": ["Art.32"]
        }
    },
    "logging": {
        "name": "Security Logging",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.8.15", "A.8.16", "A.8.17"],
            "SOC2": ["CC7.2", "CC7.3"],
            "PCI_DSS": ["10.1", "10.2", "10.3", "10.4", "10.5"],
            "NIST_CSF": ["DE.CM-1", "DE.CM-3", "DE.AE-3"],
            "HIPAA": ["164.312(b)"],
            "GDPR": ["Art.30"]
        }
    },
    "incident_response": {
        "name": "Incident Response",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.5.24", "A.5.25", "A.5.26", "A.5.27", "A.6.8"],
            "SOC2": ["CC7.3", "CC7.4", "CC7.5"],
            "PCI_DSS": ["12.10", "12.10.1", "12.10.2"],
            "NIST_CSF": ["RS.RP-1", "RS.CO-1", "RS.AN-1", "RS.MI-1"],
            "HIPAA": ["164.308(a)(6)"],
            "GDPR": ["Art.33", "Art.34"]
        }
    },
    "vulnerability_management": {
        "name": "Vulnerability Management",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.8.8"],
            "SOC2": ["CC7.1"],
            "PCI_DSS": ["6.3", "11.2", "11.3"],
            "NIST_CSF": ["DE.CM-8", "ID.RA-1", "RS.MI-3"],
            "HIPAA": ["164.308(a)(1)(ii)(A)"],
            "GDPR": ["Art.32"]
        }
    },
    "change_management": {
        "name": "Change Management",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.8.32"],
            "SOC2": ["CC8.1"],
            "PCI_DSS": ["6.4", "6.4.1", "6.4.2"],
            "NIST_CSF": ["PR.IP-3"],
            "HIPAA": ["164.308(a)(8)"],
            "GDPR": ["Art.32"]
        }
    },
    "backup": {
        "name": "Data Backup",
        "category": "Technical",
        "mappings": {
            "ISO27001": ["A.8.13"],
            "SOC2": ["A1.2"],
            "PCI_DSS": ["9.5", "9.5.1"],
            "NIST_CSF": ["PR.IP-4"],
            "HIPAA": ["164.308(a)(7)(ii)(A)", "164.310(d)(1)"],
            "GDPR": ["Art.32"]
        }
    },
    "security_awareness": {
        "name": "Security Awareness Training",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.6.3"],
            "SOC2": ["CC1.4", "CC2.2"],
            "PCI_DSS": ["12.6", "12.6.1", "12.6.2"],
            "NIST_CSF": ["PR.AT-1", "PR.AT-2"],
            "HIPAA": ["164.308(a)(5)"],
            "GDPR": ["Art.39"]
        }
    },
    "vendor_management": {
        "name": "Third-Party Risk Management",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.5.19", "A.5.20", "A.5.21", "A.5.22", "A.5.23"],
            "SOC2": ["CC9.2"],
            "PCI_DSS": ["12.8", "12.8.1", "12.8.2", "12.8.3"],
            "NIST_CSF": ["ID.SC-1", "ID.SC-2", "ID.SC-3", "ID.SC-4"],
            "HIPAA": ["164.308(b)(1)", "164.314(a)"],
            "GDPR": ["Art.28"]
        }
    },
    "asset_management": {
        "name": "Asset Management",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.5.9", "A.5.10", "A.5.11", "A.5.12", "A.5.13"],
            "SOC2": ["CC6.1"],
            "PCI_DSS": ["2.4", "9.9", "12.3"],
            "NIST_CSF": ["ID.AM-1", "ID.AM-2", "ID.AM-3", "ID.AM-4", "ID.AM-5"],
            "HIPAA": ["164.310(d)(1)"],
            "GDPR": ["Art.30"]
        }
    },
    "physical_security": {
        "name": "Physical Security",
        "category": "Physical",
        "mappings": {
            "ISO27001": ["A.7.1", "A.7.2", "A.7.3", "A.7.4", "A.7.5"],
            "SOC2": ["CC6.4", "CC6.5"],
            "PCI_DSS": ["9.1", "9.2", "9.3", "9.4"],
            "NIST_CSF": ["PR.AC-2", "PR.IP-5", "PR.IP-6"],
            "HIPAA": ["164.310(a)", "164.310(b)", "164.310(c)"],
            "GDPR": ["Art.32"]
        }
    },
    "data_classification": {
        "name": "Data Classification",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.5.12", "A.5.13"],
            "SOC2": ["CC6.1"],
            "PCI_DSS": ["3.1", "9.6"],
            "NIST_CSF": ["ID.AM-5", "PR.DS-1"],
            "HIPAA": ["164.312(c)(1)"],
            "GDPR": ["Art.5", "Art.9"]
        }
    },
    "business_continuity": {
        "name": "Business Continuity",
        "category": "Administrative",
        "mappings": {
            "ISO27001": ["A.5.29", "A.5.30"],
            "SOC2": ["A1.1", "A1.2", "A1.3"],
            "PCI_DSS": ["12.10.1"],
            "NIST_CSF": ["PR.IP-9", "PR.IP-10", "RC.RP-1"],
            "HIPAA": ["164.308(a)(7)"],
            "GDPR": ["Art.32"]
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Control:
    id: str
    name: str
    description: str
    category: str
    implementation_status: str
    owner: str
    frameworks: Dict[str, List[str]]
    evidence: List[str] = field(default_factory=list)
    last_review: str = ""
    next_review: str = ""
    notes: str = ""

# ══════════════════════════════════════════════════════════════════════════════
# CONTROL MAPPER CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ControlMapper:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.controls_path = self.workspace / "controls"
        self.mappings_path = self.controls_path / "mappings"
        
    def find_control_by_reference(self, reference: str) -> List[Dict]:
        """Find controls that map to a specific framework reference"""
        results = []
        reference_upper = reference.upper().replace("-", "_").replace(" ", "")
        
        for ctrl_id, ctrl_data in CONTROL_MAPPINGS.items():
            for framework, refs in ctrl_data["mappings"].items():
                for ref in refs:
                    ref_normalized = ref.upper().replace("-", "_").replace(" ", "").replace(".", "")
                    if reference_upper.replace(".", "") in ref_normalized or ref_normalized in reference_upper.replace(".", ""):
                        results.append({
                            "control_id": ctrl_id,
                            "control_name": ctrl_data["name"],
                            "category": ctrl_data["category"],
                            "framework": framework,
                            "reference": ref,
                            "all_mappings": ctrl_data["mappings"]
                        })
        
        return results
    
    def get_control_mappings(self, control_name: str) -> Optional[Dict]:
        """Get all framework mappings for a control"""
        control_key = control_name.lower().replace(" ", "_").replace("-", "_")
        
        # Direct match
        if control_key in CONTROL_MAPPINGS:
            return CONTROL_MAPPINGS[control_key]
        
        # Partial match
        for key, data in CONTROL_MAPPINGS.items():
            if control_key in key or key in control_key:
                return data
            if control_key in data["name"].lower():
                return data
        
        return None
    
    def map_control(self, control_name: str) -> None:
        """Display control mappings across frameworks"""
        mapping = self.get_control_mappings(control_name)
        
        if not mapping:
            console.print(f"[yellow]Control not found: {control_name}[/yellow]")
            console.print("\n[cyan]Available controls:[/cyan]")
            for key, data in CONTROL_MAPPINGS.items():
                console.print(f"  • {data['name']}")
            return
        
        console.print(Panel.fit(
            f"[bold white]⚪ CONTROL MAPPING: {mapping['name']}[/bold white]",
            border_style="white"
        ))
        
        console.print(f"\n[cyan]Category:[/cyan] {mapping['category']}")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Framework", width=15)
        table.add_column("References", width=50)
        
        for framework, refs in mapping["mappings"].items():
            table.add_row(
                framework.replace("_", " "),
                ", ".join(refs)
            )
        
        console.print(table)
    
    def find_equivalent_controls(self, framework: str, reference: str) -> None:
        """Find equivalent controls in other frameworks"""
        results = self.find_control_by_reference(reference)
        
        if not results:
            console.print(f"[yellow]No mappings found for: {reference}[/yellow]")
            return
        
        console.print(Panel.fit(
            f"[bold white]⚪ EQUIVALENT CONTROLS: {reference}[/bold white]",
            border_style="white"
        ))
        
        for result in results:
            console.print(f"\n[bold cyan]{result['control_name']}[/bold cyan] ({result['category']})")
            
            table = Table(show_header=True, header_style="bold")
            table.add_column("Framework", width=15)
            table.add_column("References", width=50)
            
            for fw, refs in result["all_mappings"].items():
                highlight = "bold green" if fw == framework.upper().replace("-", "_") else ""
                refs_str = ", ".join(refs)
                if highlight:
                    refs_str = f"[{highlight}]{refs_str}[/{highlight}]"
                table.add_row(fw.replace("_", " "), refs_str)
            
            console.print(table)
    
    def list_all_controls(self) -> None:
        """List all available control mappings"""
        console.print(Panel.fit(
            "[bold white]⚪ CONTROL MAPPINGS LIBRARY[/bold white]",
            border_style="white"
        ))
        
        # Group by category
        categories = {}
        for ctrl_id, ctrl_data in CONTROL_MAPPINGS.items():
            cat = ctrl_data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ctrl_data)
        
        for category, controls in categories.items():
            console.print(f"\n[bold cyan]{category} Controls[/bold cyan]")
            
            table = Table(show_header=True, header_style="bold")
            table.add_column("Control", width=30)
            table.add_column("Frameworks", width=50)
            
            for ctrl in controls:
                frameworks = ", ".join(ctrl["mappings"].keys())
                table.add_row(ctrl["name"], frameworks.replace("_", " "))
            
            console.print(table)
    
    def generate_mapping_matrix(self, output_format: str = "console") -> str:
        """Generate a control mapping matrix"""
        frameworks = ["ISO27001", "SOC2", "PCI_DSS", "NIST_CSF", "HIPAA", "GDPR"]
        
        if output_format == "console":
            console.print(Panel.fit(
                "[bold white]⚪ CONTROL MAPPING MATRIX[/bold white]",
                border_style="white"
            ))
            
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Control", width=25)
            for fw in frameworks:
                table.add_column(fw.replace("_", " "), width=12)
            
            for ctrl_id, ctrl_data in CONTROL_MAPPINGS.items():
                row = [ctrl_data["name"][:25]]
                for fw in frameworks:
                    refs = ctrl_data["mappings"].get(fw, [])
                    if refs:
                        row.append(f"[green]✓ ({len(refs)})[/green]")
                    else:
                        row.append("[dim]—[/dim]")
                table.add_row(*row)
            
            console.print(table)
            return "Displayed"
        
        elif output_format == "markdown":
            lines = ["# Control Mapping Matrix", ""]
            header = "| Control | " + " | ".join(fw.replace("_", " ") for fw in frameworks) + " |"
            separator = "|" + "|".join(["---"] * (len(frameworks) + 1)) + "|"
            lines.extend([header, separator])
            
            for ctrl_id, ctrl_data in CONTROL_MAPPINGS.items():
                row = [ctrl_data["name"]]
                for fw in frameworks:
                    refs = ctrl_data["mappings"].get(fw, [])
                    row.append(", ".join(refs[:2]) if refs else "—")
                lines.append("| " + " | ".join(row) + " |")
            
            content = "\n".join(lines)
            
            self.mappings_path.mkdir(parents=True, exist_ok=True)
            filepath = self.mappings_path / "control_matrix.md"
            with open(filepath, 'w') as f:
                f.write(content)
            
            console.print(f"[green]✓ Matrix saved to: {filepath}[/green]")
            return str(filepath)
        
        elif output_format == "yaml":
            self.mappings_path.mkdir(parents=True, exist_ok=True)
            filepath = self.mappings_path / "framework_mappings.yaml"
            
            data = {"mappings": []}
            for ctrl_id, ctrl_data in CONTROL_MAPPINGS.items():
                data["mappings"].append({
                    "control_name": ctrl_data["name"],
                    "category": ctrl_data["category"],
                    "frameworks": ctrl_data["mappings"]
                })
            
            with open(filepath, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
            
            console.print(f"[green]✓ Mappings saved to: {filepath}[/green]")
            return str(filepath)
        
        return ""
    
    def create_control(self, interactive: bool = True) -> Optional[Control]:
        """Create a new control with mappings"""
        console.print(Panel.fit(
            "[bold white]⚪ CREATE NEW CONTROL[/bold white]",
            border_style="white"
        ))
        
        if not interactive:
            return None
        
        ctrl_id = Prompt.ask("Control ID (e.g., CTRL-001)")
        name = Prompt.ask("Control Name")
        description = Prompt.ask("Description")
        category = Prompt.ask("Category", choices=["Technical", "Administrative", "Physical"])
        status = Prompt.ask("Implementation Status", 
                           choices=["implemented", "partial", "planned", "not_implemented"],
                           default="planned")
        owner = Prompt.ask("Control Owner")
        
        # Framework mappings
        frameworks = {}
        console.print("\n[cyan]Add framework mappings (empty to finish):[/cyan]")
        
        for fw in ["ISO27001", "SOC2", "PCI_DSS", "NIST_CSF", "HIPAA", "GDPR"]:
            refs = Prompt.ask(f"{fw} references (comma-separated)", default="")
            if refs:
                frameworks[fw] = [r.strip() for r in refs.split(",")]
        
        control = Control(
            id=ctrl_id,
            name=name,
            description=description,
            category=category,
            implementation_status=status,
            owner=owner,
            frameworks=frameworks,
            last_review=datetime.now().strftime("%Y-%m-%d"),
            next_review=(datetime.now().replace(month=datetime.now().month + 6)).strftime("%Y-%m-%d")
        )
        
        # Save control
        category_path = self.controls_path / category.lower()
        category_path.mkdir(parents=True, exist_ok=True)
        
        filepath = category_path / f"{ctrl_id}.yaml"
        
        control_dict = {
            "id": control.id,
            "name": control.name,
            "description": control.description,
            "category": control.category,
            "implementation_status": control.implementation_status,
            "owner": control.owner,
            "frameworks": control.frameworks,
            "evidence": control.evidence,
            "last_review": control.last_review,
            "next_review": control.next_review,
            "notes": control.notes
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(control_dict, f, default_flow_style=False)
        
        console.print(f"\n[green]✓ Control saved to: {filepath}[/green]")
        
        return control

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--map', '-m', 'map_control', type=str, help='Map a control across frameworks')
@click.option('--find', '-f', type=str, help='Find control by framework reference')
@click.option('--list', '-l', 'list_controls', is_flag=True, help='List all control mappings')
@click.option('--matrix', is_flag=True, help='Generate mapping matrix')
@click.option('--create', '-c', is_flag=True, help='Create new control')
@click.option('--format', '-o', type=click.Choice(['console', 'markdown', 'yaml']),
              default='console', help='Output format')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.', help='Workspace path')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Control Mapper')
def main(map_control: str, find: str, list_controls: bool, matrix: bool,
         create: bool, format: str, workspace: str):
    """
    ⚪ WHITE TEAM GRC - Control Mapper Tool
    
    Mapea controles entre múltiples frameworks de compliance.
    """
    mapper = ControlMapper(workspace)
    
    if map_control:
        mapper.map_control(map_control)
    elif find:
        # Parse framework:reference format
        if ":" in find:
            framework, reference = find.split(":", 1)
        else:
            framework, reference = "ISO27001", find
        mapper.find_equivalent_controls(framework, reference)
    elif list_controls:
        mapper.list_all_controls()
    elif matrix:
        mapper.generate_mapping_matrix(format)
    elif create:
        mapper.create_control()
    else:
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - Control Mapper[/bold white]",
            border_style="white"
        ))
        console.print("\n[cyan]Usage:[/cyan]")
        console.print("  --map CONTROL      Map control across frameworks")
        console.print("  --find REF         Find control by reference (e.g., ISO27001:A.8.5)")
        console.print("  --list             List all control mappings")
        console.print("  --matrix           Generate mapping matrix")
        console.print("  --create           Create new control")
        console.print("\n[dim]Example: python control_mapper.py --map 'Multi-Factor Authentication'[/dim]")
        console.print("[dim]Example: python control_mapper.py --find 'ISO27001:A.8.5'[/dim]")

if __name__ == '__main__':
    main()
