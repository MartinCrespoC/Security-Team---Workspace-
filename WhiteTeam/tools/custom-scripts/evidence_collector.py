#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Evidence Collector Tool
Gestiona la recolección y organización de evidencia de compliance
"""

import os
import sys
import json
import yaml
import hashlib
import shutil
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
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class EvidenceItem:
    id: str
    control_id: str
    control_name: str
    type: str  # screenshot, log, config, document, report
    description: str
    file_path: str
    file_hash: str
    collected_by: str
    collected_date: str
    period_start: str
    period_end: str
    source_system: str
    frameworks: List[str]
    status: str = "current"  # current, archived, expired
    notes: str = ""

@dataclass
class EvidenceRegister:
    last_updated: str
    total_items: int
    items: List[EvidenceItem]

# ══════════════════════════════════════════════════════════════════════════════
# EVIDENCE REQUIREMENTS BY FRAMEWORK
# ══════════════════════════════════════════════════════════════════════════════

EVIDENCE_REQUIREMENTS = {
    "ISO27001": {
        "A.5.1": {
            "name": "Policies for information security",
            "evidence_types": ["document"],
            "examples": ["Information security policy", "Policy review records", "Approval signatures"]
        },
        "A.6.3": {
            "name": "Information security awareness",
            "evidence_types": ["document", "report"],
            "examples": ["Training materials", "Completion records", "Quiz results"]
        },
        "A.8.2": {
            "name": "Privileged access rights",
            "evidence_types": ["screenshot", "log", "config"],
            "examples": ["PAM configuration", "Access logs", "Review records"]
        },
        "A.8.5": {
            "name": "Secure authentication",
            "evidence_types": ["screenshot", "config"],
            "examples": ["MFA configuration", "Authentication policy", "Enrollment reports"]
        },
        "A.8.15": {
            "name": "Logging",
            "evidence_types": ["screenshot", "log", "config"],
            "examples": ["SIEM configuration", "Log samples", "Retention settings"]
        }
    },
    "SOC2": {
        "CC6.1": {
            "name": "Logical access security",
            "evidence_types": ["screenshot", "config", "document"],
            "examples": ["Access control configuration", "User provisioning process", "Access matrix"]
        },
        "CC6.4": {
            "name": "Access review",
            "evidence_types": ["document", "screenshot"],
            "examples": ["Access review reports", "Recertification records", "Exception documentation"]
        },
        "CC7.2": {
            "name": "Monitoring",
            "evidence_types": ["screenshot", "log", "report"],
            "examples": ["Monitoring dashboards", "Alert configurations", "Incident reports"]
        },
        "CC7.4": {
            "name": "Incident response",
            "evidence_types": ["document", "report"],
            "examples": ["IR plan", "Incident tickets", "Post-mortem reports"]
        }
    },
    "PCI-DSS": {
        "8.3": {
            "name": "Strong authentication",
            "evidence_types": ["screenshot", "config"],
            "examples": ["MFA configuration", "Password policy", "Authentication logs"]
        },
        "10.1": {
            "name": "Audit trails",
            "evidence_types": ["screenshot", "log", "config"],
            "examples": ["Logging configuration", "Log samples", "Retention policy"]
        },
        "11.2": {
            "name": "Vulnerability scans",
            "evidence_types": ["report"],
            "examples": ["Scan reports", "Remediation evidence", "Quarterly scan schedule"]
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# EVIDENCE COLLECTOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

class EvidenceCollector:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.evidence_path = self.workspace / "evidence"
        self.register_file = self.evidence_path / "register.yaml"
        self.register: Optional[EvidenceRegister] = None
        
    def load_register(self) -> EvidenceRegister:
        """Load evidence register"""
        if self.register_file.exists():
            try:
                with open(self.register_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data:
                        items = []
                        for item_data in data.get('items', []):
                            items.append(EvidenceItem(**item_data))
                        self.register = EvidenceRegister(
                            last_updated=data.get('last_updated', ''),
                            total_items=data.get('total_items', 0),
                            items=items
                        )
                        return self.register
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load register: {e}[/yellow]")
        
        self.register = EvidenceRegister(
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_items=0,
            items=[]
        )
        return self.register
    
    def save_register(self) -> None:
        """Save evidence register"""
        if not self.register:
            return
        
        self.evidence_path.mkdir(parents=True, exist_ok=True)
        
        data = {
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_items': len(self.register.items),
            'items': [
                {
                    'id': item.id,
                    'control_id': item.control_id,
                    'control_name': item.control_name,
                    'type': item.type,
                    'description': item.description,
                    'file_path': item.file_path,
                    'file_hash': item.file_hash,
                    'collected_by': item.collected_by,
                    'collected_date': item.collected_date,
                    'period_start': item.period_start,
                    'period_end': item.period_end,
                    'source_system': item.source_system,
                    'frameworks': item.frameworks,
                    'status': item.status,
                    'notes': item.notes
                }
                for item in self.register.items
            ]
        }
        
        with open(self.register_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    def calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def list_requirements(self, framework: str = None) -> None:
        """List evidence requirements"""
        console.print(Panel.fit(
            "[bold white]⚪ EVIDENCE REQUIREMENTS[/bold white]",
            border_style="white"
        ))
        
        frameworks = [framework] if framework else EVIDENCE_REQUIREMENTS.keys()
        
        for fw in frameworks:
            if fw not in EVIDENCE_REQUIREMENTS:
                continue
            
            console.print(f"\n[bold cyan]{fw}[/bold cyan]")
            
            table = Table(show_header=True, header_style="bold")
            table.add_column("Control", width=12)
            table.add_column("Name", width=30)
            table.add_column("Evidence Types", width=20)
            table.add_column("Examples", width=35)
            
            for ctrl_id, ctrl_data in EVIDENCE_REQUIREMENTS[fw].items():
                table.add_row(
                    ctrl_id,
                    ctrl_data['name'],
                    ", ".join(ctrl_data['evidence_types']),
                    ", ".join(ctrl_data['examples'][:2])
                )
            
            console.print(table)
    
    def collect_evidence(self, source_file: str, control_id: str, 
                        interactive: bool = True) -> Optional[EvidenceItem]:
        """Collect and register evidence"""
        source_path = Path(source_file)
        
        if not source_path.exists():
            console.print(f"[red]File not found: {source_file}[/red]")
            return None
        
        self.load_register()
        
        console.print(Panel.fit(
            "[bold white]⚪ COLLECT EVIDENCE[/bold white]",
            border_style="white"
        ))
        
        if interactive:
            return self._interactive_collection(source_path, control_id)
        else:
            return self._auto_collection(source_path, control_id)
    
    def _interactive_collection(self, source_path: Path, control_id: str) -> EvidenceItem:
        """Interactive evidence collection"""
        console.print(f"\n[cyan]Source File:[/cyan] {source_path}")
        console.print(f"[cyan]Control ID:[/cyan] {control_id}")
        
        # Determine evidence type from extension
        ext = source_path.suffix.lower()
        type_map = {
            '.png': 'screenshot', '.jpg': 'screenshot', '.jpeg': 'screenshot',
            '.log': 'log', '.txt': 'log', '.csv': 'log',
            '.conf': 'config', '.cfg': 'config', '.yaml': 'config', '.json': 'config',
            '.pdf': 'document', '.docx': 'document', '.md': 'document'
        }
        evidence_type = type_map.get(ext, 'document')
        evidence_type = Prompt.ask("Evidence Type", 
                                   choices=['screenshot', 'log', 'config', 'document', 'report'],
                                   default=evidence_type)
        
        control_name = Prompt.ask("Control Name", default=f"Control {control_id}")
        description = Prompt.ask("Description")
        source_system = Prompt.ask("Source System", default="Unknown")
        collected_by = Prompt.ask("Collected By", default=os.getenv("USER", "Auditor"))
        
        period_start = Prompt.ask("Period Start (YYYY-MM-DD)", 
                                  default=(datetime.now().replace(day=1)).strftime("%Y-%m-%d"))
        period_end = Prompt.ask("Period End (YYYY-MM-DD)",
                               default=datetime.now().strftime("%Y-%m-%d"))
        
        frameworks = Prompt.ask("Frameworks (comma-separated)", default="ISO27001").split(",")
        frameworks = [f.strip() for f in frameworks]
        
        notes = Prompt.ask("Notes", default="")
        
        # Generate evidence ID
        evidence_id = f"EVD-{control_id.replace('.', '')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine destination path
        type_dirs = {
            'screenshot': 'screenshots',
            'log': 'logs',
            'config': 'configs',
            'document': 'documents',
            'report': 'documents'
        }
        
        quarter = f"Q{(datetime.now().month - 1) // 3 + 1}"
        year = datetime.now().year
        
        dest_dir = self.evidence_path / type_dirs[evidence_type] / f"{year}-{quarter}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        new_filename = f"EVD-{control_id}-{datetime.now().strftime('%Y%m%d')}-{description[:20].replace(' ', '_')}{source_path.suffix}"
        dest_path = dest_dir / new_filename
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        
        # Calculate hash
        file_hash = self.calculate_hash(dest_path)
        
        # Create evidence item
        evidence = EvidenceItem(
            id=evidence_id,
            control_id=control_id,
            control_name=control_name,
            type=evidence_type,
            description=description,
            file_path=str(dest_path.relative_to(self.workspace)),
            file_hash=f"sha256:{file_hash}",
            collected_by=collected_by,
            collected_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            period_start=period_start,
            period_end=period_end,
            source_system=source_system,
            frameworks=frameworks,
            notes=notes
        )
        
        # Add to register
        self.register.items.append(evidence)
        self.save_register()
        
        console.print(f"\n[green]✓ Evidence collected: {evidence_id}[/green]")
        console.print(f"[green]✓ Saved to: {dest_path}[/green]")
        
        return evidence
    
    def _auto_collection(self, source_path: Path, control_id: str) -> EvidenceItem:
        """Automatic evidence collection with defaults"""
        ext = source_path.suffix.lower()
        type_map = {
            '.png': 'screenshot', '.jpg': 'screenshot',
            '.log': 'log', '.txt': 'log',
            '.conf': 'config', '.yaml': 'config',
            '.pdf': 'document', '.md': 'document'
        }
        evidence_type = type_map.get(ext, 'document')
        
        evidence_id = f"EVD-{control_id.replace('.', '')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        type_dirs = {'screenshot': 'screenshots', 'log': 'logs', 'config': 'configs', 'document': 'documents'}
        quarter = f"Q{(datetime.now().month - 1) // 3 + 1}"
        year = datetime.now().year
        
        dest_dir = self.evidence_path / type_dirs.get(evidence_type, 'documents') / f"{year}-{quarter}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        new_filename = f"EVD-{control_id}-{datetime.now().strftime('%Y%m%d')}{source_path.suffix}"
        dest_path = dest_dir / new_filename
        
        shutil.copy2(source_path, dest_path)
        file_hash = self.calculate_hash(dest_path)
        
        evidence = EvidenceItem(
            id=evidence_id,
            control_id=control_id,
            control_name=f"Control {control_id}",
            type=evidence_type,
            description=source_path.stem,
            file_path=str(dest_path.relative_to(self.workspace)),
            file_hash=f"sha256:{file_hash}",
            collected_by=os.getenv("USER", "Auditor"),
            collected_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            period_start=(datetime.now().replace(day=1)).strftime("%Y-%m-%d"),
            period_end=datetime.now().strftime("%Y-%m-%d"),
            source_system="Unknown",
            frameworks=["ISO27001"]
        )
        
        self.register.items.append(evidence)
        self.save_register()
        
        return evidence
    
    def list_evidence(self, control_id: str = None, framework: str = None) -> None:
        """List collected evidence"""
        self.load_register()
        
        console.print(Panel.fit(
            "[bold white]⚪ EVIDENCE REGISTER[/bold white]",
            border_style="white"
        ))
        
        items = self.register.items
        
        if control_id:
            items = [i for i in items if i.control_id == control_id]
        
        if framework:
            items = [i for i in items if framework in i.frameworks]
        
        if not items:
            console.print("[yellow]No evidence found[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", width=25)
        table.add_column("Control", width=10)
        table.add_column("Type", width=12)
        table.add_column("Description", width=25)
        table.add_column("Date", width=12)
        table.add_column("Status", width=10)
        
        for item in items:
            status_color = "green" if item.status == "current" else "yellow" if item.status == "archived" else "red"
            table.add_row(
                item.id,
                item.control_id,
                item.type,
                item.description[:25],
                item.collected_date[:10],
                f"[{status_color}]{item.status}[/{status_color}]"
            )
        
        console.print(table)
        console.print(f"\n[dim]Total: {len(items)} items[/dim]")
    
    def verify_evidence(self, evidence_id: str) -> bool:
        """Verify evidence integrity"""
        self.load_register()
        
        item = next((i for i in self.register.items if i.id == evidence_id), None)
        
        if not item:
            console.print(f"[red]Evidence not found: {evidence_id}[/red]")
            return False
        
        file_path = self.workspace / item.file_path
        
        if not file_path.exists():
            console.print(f"[red]File not found: {file_path}[/red]")
            return False
        
        current_hash = f"sha256:{self.calculate_hash(file_path)}"
        
        if current_hash == item.file_hash:
            console.print(f"[green]✓ Evidence integrity verified: {evidence_id}[/green]")
            return True
        else:
            console.print(f"[red]✗ Evidence integrity FAILED: {evidence_id}[/red]")
            console.print(f"[red]  Expected: {item.file_hash}[/red]")
            console.print(f"[red]  Got: {current_hash}[/red]")
            return False

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--collect', '-c', type=str, help='Collect evidence from file')
@click.option('--control', '-ctrl', type=str, help='Control ID for evidence')
@click.option('--list', '-l', 'list_evidence', is_flag=True, help='List collected evidence')
@click.option('--requirements', '-r', is_flag=True, help='Show evidence requirements')
@click.option('--framework', '-f', type=str, help='Filter by framework')
@click.option('--verify', '-v', type=str, help='Verify evidence integrity')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.', help='Workspace path')
@click.option('--interactive/--no-interactive', '-i', default=True, help='Interactive mode')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Evidence Collector')
def main(collect: str, control: str, list_evidence: bool, requirements: bool,
         framework: str, verify: str, workspace: str, interactive: bool):
    """
    ⚪ WHITE TEAM GRC - Evidence Collector Tool
    
    Gestiona la recolección y organización de evidencia de compliance.
    """
    collector = EvidenceCollector(workspace)
    
    if requirements:
        collector.list_requirements(framework)
    elif collect and control:
        collector.collect_evidence(collect, control, interactive)
    elif list_evidence:
        collector.list_evidence(control, framework)
    elif verify:
        collector.verify_evidence(verify)
    else:
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - Evidence Collector[/bold white]",
            border_style="white"
        ))
        console.print("\n[cyan]Usage:[/cyan]")
        console.print("  --collect FILE --control ID   Collect evidence")
        console.print("  --list                        List evidence")
        console.print("  --requirements                Show requirements")
        console.print("  --verify ID                   Verify integrity")
        console.print("\n[dim]Example: python evidence_collector.py --collect screenshot.png --control A.8.5[/dim]")

if __name__ == '__main__':
    main()
