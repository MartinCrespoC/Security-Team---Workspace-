#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Risk Assessment Tool
Evalúa y calcula riesgos de seguridad con metodología cuantitativa
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich import print as rprint
except ImportError:
    print("Installing required packages...")
    os.system("pip install click rich pyyaml")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich import print as rprint

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

class TreatmentStrategy(Enum):
    MITIGATE = "mitigate"
    TRANSFER = "transfer"
    ACCEPT = "accept"
    AVOID = "avoid"

class RiskCategory(Enum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    COMPLIANCE = "compliance"
    TECHNOLOGY = "technology"
    THIRD_PARTY = "third_party"

class RiskStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    ACCEPTED = "accepted"

@dataclass
class RiskScore:
    likelihood: int  # 1-5
    impact: int      # 1-5
    score: int       # likelihood * impact
    level: RiskLevel
    
    @classmethod
    def calculate(cls, likelihood: int, impact: int) -> 'RiskScore':
        score = likelihood * impact
        if score >= 20:
            level = RiskLevel.CRITICAL
        elif score >= 15:
            level = RiskLevel.HIGH
        elif score >= 8:
            level = RiskLevel.MEDIUM
        elif score >= 4:
            level = RiskLevel.LOW
        else:
            level = RiskLevel.VERY_LOW
        return cls(likelihood=likelihood, impact=impact, score=score, level=level)

@dataclass
class Control:
    id: str
    name: str
    effectiveness: float  # 0-100

@dataclass
class Treatment:
    strategy: TreatmentStrategy
    actions: List[str]
    owner: str
    due_date: str
    status: str = "pending"

@dataclass
class Risk:
    id: str
    title: str
    description: str
    category: RiskCategory
    asset: str
    threat: str
    vulnerability: str
    inherent_risk: RiskScore
    controls: List[Control]
    residual_risk: RiskScore
    treatment: Optional[Treatment]
    status: RiskStatus
    created_date: str
    last_updated: str
    owner: Optional[str] = None
    notes: str = ""

# ══════════════════════════════════════════════════════════════════════════════
# RISK MATRIX VISUALIZATION
# ══════════════════════════════════════════════════════════════════════════════

RISK_MATRIX = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RISK ASSESSMENT MATRIX                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LIKELIHOOD                                                                 │
│       │                                                                     │
│   5   │  5    10    15    20    25                                         │
│  Muy  │  ┌─────┬─────┬─────┬─────┬─────┐                                   │
│  Alta │  │ MED │ MED │HIGH │CRIT │CRIT │                                   │
│       │  └─────┴─────┴─────┴─────┴─────┘                                   │
│   4   │  4     8    12    16    20                                         │
│  Alta │  ┌─────┬─────┬─────┬─────┬─────┐                                   │
│       │  │ LOW │ MED │ MED │HIGH │CRIT │                                   │
│       │  └─────┴─────┴─────┴─────┴─────┘                                   │
│   3   │  3     6     9    12    15                                         │
│ Media │  ┌─────┬─────┬─────┬─────┬─────┐                                   │
│       │  │ LOW │ LOW │ MED │ MED │HIGH │                                   │
│       │  └─────┴─────┴─────┴─────┴─────┘                                   │
│   2   │  2     4     6     8    10                                         │
│  Baja │  ┌─────┬─────┬─────┬─────┬─────┐                                   │
│       │  │VLOW │ LOW │ LOW │ MED │ MED │                                   │
│       │  └─────┴─────┴─────┴─────┴─────┘                                   │
│   1   │  1     2     3     4     5                                         │
│  Muy  │  ┌─────┬─────┬─────┬─────┬─────┐                                   │
│  Baja │  │VLOW │VLOW │ LOW │ LOW │ MED │                                   │
│       │  └─────┴─────┴─────┴─────┴─────┘                                   │
│       └────────────────────────────────────────────────────────────────    │
│              1        2        3        4        5                          │
│            Muy      Bajo    Medio     Alto    Muy                          │
│            Bajo                               Alto                          │
│                           IMPACT                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

LIKELIHOOD_SCALE = {
    1: "Muy Baja - Raro (< 10% probabilidad)",
    2: "Baja - Improbable (10-30% probabilidad)",
    3: "Media - Posible (30-60% probabilidad)",
    4: "Alta - Probable (60-90% probabilidad)",
    5: "Muy Alta - Casi seguro (> 90% probabilidad)"
}

IMPACT_SCALE = {
    1: "Muy Bajo - Impacto insignificante",
    2: "Bajo - Impacto menor, fácil recuperación",
    3: "Medio - Impacto moderado, requiere esfuerzo",
    4: "Alto - Impacto significativo, daño considerable",
    5: "Muy Alto - Impacto catastrófico, daño severo"
}

# ══════════════════════════════════════════════════════════════════════════════
# RISK ASSESSOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

class RiskAssessor:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.risks_path = self.workspace / "risks"
        self.register_path = self.risks_path / "register"
        self.assessments_path = self.risks_path / "assessments"
        self.risks: List[Risk] = []
        
    def load_risks(self) -> List[Risk]:
        """Load existing risks from register"""
        self.risks = []
        if self.register_path.exists():
            for file in self.register_path.glob("*.yaml"):
                try:
                    with open(file, 'r') as f:
                        data = yaml.safe_load(f)
                        if data:
                            risk = self._dict_to_risk(data)
                            self.risks.append(risk)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not load {file}: {e}[/yellow]")
        return self.risks
    
    def _dict_to_risk(self, data: Dict) -> Risk:
        """Convert dictionary to Risk object"""
        inherent = data.get('inherent_risk', {})
        residual = data.get('residual_risk', {})
        
        controls = []
        for ctrl in data.get('controls', []):
            controls.append(Control(
                id=ctrl.get('id', ''),
                name=ctrl.get('name', ''),
                effectiveness=ctrl.get('effectiveness', 0)
            ))
        
        treatment_data = data.get('treatment')
        treatment = None
        if treatment_data:
            treatment = Treatment(
                strategy=TreatmentStrategy(treatment_data.get('strategy', 'mitigate')),
                actions=treatment_data.get('actions', []),
                owner=treatment_data.get('owner', ''),
                due_date=treatment_data.get('due_date', ''),
                status=treatment_data.get('status', 'pending')
            )
        
        return Risk(
            id=data.get('id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            category=RiskCategory(data.get('category', 'operational')),
            asset=data.get('asset', ''),
            threat=data.get('threat', ''),
            vulnerability=data.get('vulnerability', ''),
            inherent_risk=RiskScore.calculate(
                inherent.get('likelihood', 3),
                inherent.get('impact', 3)
            ),
            controls=controls,
            residual_risk=RiskScore.calculate(
                residual.get('likelihood', 3),
                residual.get('impact', 3)
            ),
            treatment=treatment,
            status=RiskStatus(data.get('status', 'open')),
            created_date=data.get('created_date', ''),
            last_updated=data.get('last_updated', ''),
            owner=data.get('owner'),
            notes=data.get('notes', '')
        )
    
    def calculate_residual_risk(self, inherent: RiskScore, controls: List[Control]) -> RiskScore:
        """Calculate residual risk based on control effectiveness"""
        if not controls:
            return inherent
        
        # Average control effectiveness
        avg_effectiveness = sum(c.effectiveness for c in controls) / len(controls) / 100
        
        # Reduce likelihood and impact based on effectiveness
        residual_likelihood = max(1, int(inherent.likelihood * (1 - avg_effectiveness * 0.7)))
        residual_impact = max(1, int(inherent.impact * (1 - avg_effectiveness * 0.3)))
        
        return RiskScore.calculate(residual_likelihood, residual_impact)
    
    def recommend_treatment(self, risk: RiskScore) -> TreatmentStrategy:
        """Recommend treatment strategy based on risk level"""
        if risk.level == RiskLevel.CRITICAL:
            return TreatmentStrategy.AVOID
        elif risk.level == RiskLevel.HIGH:
            return TreatmentStrategy.MITIGATE
        elif risk.level == RiskLevel.MEDIUM:
            return TreatmentStrategy.MITIGATE
        elif risk.level == RiskLevel.LOW:
            return TreatmentStrategy.ACCEPT
        else:
            return TreatmentStrategy.ACCEPT
    
    def create_risk(self, interactive: bool = True) -> Risk:
        """Create a new risk assessment"""
        console.print(Panel.fit(
            "[bold white]⚪ NEW RISK ASSESSMENT[/bold white]",
            border_style="white"
        ))
        
        if interactive:
            return self._interactive_risk_creation()
        else:
            return self._default_risk_creation()
    
    def _interactive_risk_creation(self) -> Risk:
        """Interactive risk creation wizard"""
        console.print("\n[cyan]Step 1: Risk Identification[/cyan]\n")
        
        title = Prompt.ask("Risk Title")
        description = Prompt.ask("Description")
        
        console.print("\n[dim]Categories: strategic, operational, financial, compliance, technology, third_party[/dim]")
        category = Prompt.ask("Category", default="operational")
        
        asset = Prompt.ask("Affected Asset")
        threat = Prompt.ask("Threat Description")
        vulnerability = Prompt.ask("Vulnerability Description")
        
        console.print("\n[cyan]Step 2: Inherent Risk Assessment[/cyan]")
        console.print(RISK_MATRIX)
        
        console.print("\n[bold]Likelihood Scale:[/bold]")
        for k, v in LIKELIHOOD_SCALE.items():
            console.print(f"  {k}: {v}")
        likelihood = IntPrompt.ask("\nLikelihood (1-5)", default=3)
        likelihood = max(1, min(5, likelihood))
        
        console.print("\n[bold]Impact Scale:[/bold]")
        for k, v in IMPACT_SCALE.items():
            console.print(f"  {k}: {v}")
        impact = IntPrompt.ask("\nImpact (1-5)", default=3)
        impact = max(1, min(5, impact))
        
        inherent_risk = RiskScore.calculate(likelihood, impact)
        
        console.print(f"\n[bold]Inherent Risk Score: {inherent_risk.score} ({inherent_risk.level.value.upper()})[/bold]")
        
        console.print("\n[cyan]Step 3: Existing Controls[/cyan]\n")
        
        controls = []
        while Confirm.ask("Add a control?", default=True):
            ctrl_id = Prompt.ask("Control ID")
            ctrl_name = Prompt.ask("Control Name")
            ctrl_eff = IntPrompt.ask("Effectiveness (0-100%)", default=50)
            ctrl_eff = max(0, min(100, ctrl_eff))
            controls.append(Control(id=ctrl_id, name=ctrl_name, effectiveness=ctrl_eff))
        
        residual_risk = self.calculate_residual_risk(inherent_risk, controls)
        
        console.print(f"\n[bold]Residual Risk Score: {residual_risk.score} ({residual_risk.level.value.upper()})[/bold]")
        
        console.print("\n[cyan]Step 4: Treatment Plan[/cyan]\n")
        
        recommended = self.recommend_treatment(residual_risk)
        console.print(f"[dim]Recommended strategy: {recommended.value}[/dim]")
        
        strategy = Prompt.ask(
            "Treatment Strategy",
            choices=["mitigate", "transfer", "accept", "avoid"],
            default=recommended.value
        )
        
        actions = []
        if strategy != "accept":
            console.print("\nEnter treatment actions (empty to finish):")
            while True:
                action = Prompt.ask("Action", default="")
                if not action:
                    break
                actions.append(action)
        
        owner = Prompt.ask("Risk Owner")
        due_date = Prompt.ask("Due Date (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))
        
        treatment = Treatment(
            strategy=TreatmentStrategy(strategy),
            actions=actions,
            owner=owner,
            due_date=due_date
        )
        
        risk_id = f"RISK-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        risk = Risk(
            id=risk_id,
            title=title,
            description=description,
            category=RiskCategory(category),
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            inherent_risk=inherent_risk,
            controls=controls,
            residual_risk=residual_risk,
            treatment=treatment,
            status=RiskStatus.OPEN,
            created_date=now,
            last_updated=now,
            owner=owner
        )
        
        return risk
    
    def _default_risk_creation(self) -> Risk:
        """Create a default risk for non-interactive mode"""
        risk_id = f"RISK-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return Risk(
            id=risk_id,
            title="New Risk",
            description="Risk description pending",
            category=RiskCategory.OPERATIONAL,
            asset="TBD",
            threat="TBD",
            vulnerability="TBD",
            inherent_risk=RiskScore.calculate(3, 3),
            controls=[],
            residual_risk=RiskScore.calculate(3, 3),
            treatment=None,
            status=RiskStatus.OPEN,
            created_date=now,
            last_updated=now
        )
    
    def save_risk(self, risk: Risk) -> str:
        """Save risk to register"""
        self.register_path.mkdir(parents=True, exist_ok=True)
        
        risk_dict = {
            'id': risk.id,
            'title': risk.title,
            'description': risk.description,
            'category': risk.category.value,
            'asset': risk.asset,
            'threat': risk.threat,
            'vulnerability': risk.vulnerability,
            'inherent_risk': {
                'likelihood': risk.inherent_risk.likelihood,
                'impact': risk.inherent_risk.impact,
                'score': risk.inherent_risk.score,
                'level': risk.inherent_risk.level.value
            },
            'controls': [
                {'id': c.id, 'name': c.name, 'effectiveness': c.effectiveness}
                for c in risk.controls
            ],
            'residual_risk': {
                'likelihood': risk.residual_risk.likelihood,
                'impact': risk.residual_risk.impact,
                'score': risk.residual_risk.score,
                'level': risk.residual_risk.level.value
            },
            'treatment': {
                'strategy': risk.treatment.strategy.value,
                'actions': risk.treatment.actions,
                'owner': risk.treatment.owner,
                'due_date': risk.treatment.due_date,
                'status': risk.treatment.status
            } if risk.treatment else None,
            'status': risk.status.value,
            'created_date': risk.created_date,
            'last_updated': risk.last_updated,
            'owner': risk.owner,
            'notes': risk.notes
        }
        
        file_path = self.register_path / f"{risk.id}.yaml"
        with open(file_path, 'w') as f:
            yaml.dump(risk_dict, f, default_flow_style=False, allow_unicode=True)
        
        return str(file_path)
    
    def display_risk(self, risk: Risk):
        """Display risk details"""
        level_colors = {
            RiskLevel.CRITICAL: "red",
            RiskLevel.HIGH: "orange1",
            RiskLevel.MEDIUM: "yellow",
            RiskLevel.LOW: "green",
            RiskLevel.VERY_LOW: "blue"
        }
        
        inherent_color = level_colors[risk.inherent_risk.level]
        residual_color = level_colors[risk.residual_risk.level]
        
        console.print(Panel.fit(
            f"[bold white]{risk.id}: {risk.title}[/bold white]",
            border_style="white"
        ))
        
        table = Table(show_header=False, box=None)
        table.add_column("Field", style="cyan", width=20)
        table.add_column("Value", style="white")
        
        table.add_row("Category", risk.category.value.upper())
        table.add_row("Asset", risk.asset)
        table.add_row("Threat", risk.threat)
        table.add_row("Vulnerability", risk.vulnerability)
        table.add_row("", "")
        table.add_row("Inherent Risk", f"[{inherent_color}]{risk.inherent_risk.score} ({risk.inherent_risk.level.value.upper()})[/{inherent_color}]")
        table.add_row("  Likelihood", str(risk.inherent_risk.likelihood))
        table.add_row("  Impact", str(risk.inherent_risk.impact))
        table.add_row("", "")
        table.add_row("Controls", str(len(risk.controls)))
        for ctrl in risk.controls:
            table.add_row(f"  {ctrl.id}", f"{ctrl.name} ({ctrl.effectiveness}%)")
        table.add_row("", "")
        table.add_row("Residual Risk", f"[{residual_color}]{risk.residual_risk.score} ({risk.residual_risk.level.value.upper()})[/{residual_color}]")
        table.add_row("", "")
        if risk.treatment:
            table.add_row("Treatment", risk.treatment.strategy.value.upper())
            table.add_row("  Owner", risk.treatment.owner)
            table.add_row("  Due Date", risk.treatment.due_date)
        table.add_row("Status", risk.status.value.upper())
        
        console.print(table)
    
    def generate_register_report(self) -> None:
        """Generate risk register report"""
        self.load_risks()
        
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - RISK REGISTER[/bold white]",
            border_style="white"
        ))
        
        if not self.risks:
            console.print("[yellow]No risks found in register[/yellow]")
            return
        
        table = Table(title=f"Risk Register ({len(self.risks)} risks)", show_header=True, header_style="bold cyan")
        table.add_column("ID", width=20)
        table.add_column("Title", width=25)
        table.add_column("Category", width=12)
        table.add_column("Inherent", justify="center", width=10)
        table.add_column("Residual", justify="center", width=10)
        table.add_column("Status", width=12)
        
        level_colors = {
            RiskLevel.CRITICAL: "red",
            RiskLevel.HIGH: "orange1",
            RiskLevel.MEDIUM: "yellow",
            RiskLevel.LOW: "green",
            RiskLevel.VERY_LOW: "blue"
        }
        
        for risk in sorted(self.risks, key=lambda r: r.inherent_risk.score, reverse=True):
            inh_color = level_colors[risk.inherent_risk.level]
            res_color = level_colors[risk.residual_risk.level]
            
            table.add_row(
                risk.id,
                risk.title[:25],
                risk.category.value,
                f"[{inh_color}]{risk.inherent_risk.score}[/{inh_color}]",
                f"[{res_color}]{risk.residual_risk.score}[/{res_color}]",
                risk.status.value
            )
        
        console.print(table)
        
        # Summary
        critical = sum(1 for r in self.risks if r.residual_risk.level == RiskLevel.CRITICAL)
        high = sum(1 for r in self.risks if r.residual_risk.level == RiskLevel.HIGH)
        medium = sum(1 for r in self.risks if r.residual_risk.level == RiskLevel.MEDIUM)
        low = sum(1 for r in self.risks if r.residual_risk.level == RiskLevel.LOW)
        
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"  [red]Critical: {critical}[/red]")
        console.print(f"  [orange1]High: {high}[/orange1]")
        console.print(f"  [yellow]Medium: {medium}[/yellow]")
        console.print(f"  [green]Low: {low}[/green]")

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--new', '-n', is_flag=True, help='Create new risk assessment')
@click.option('--list', '-l', 'list_risks', is_flag=True, help='List all risks')
@click.option('--view', '-v', type=str, help='View specific risk by ID')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.', help='Workspace path')
@click.option('--interactive/--no-interactive', '-i', default=True, help='Interactive mode')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Risk Assessment')
def main(new: bool, list_risks: bool, view: str, workspace: str, interactive: bool):
    """
    ⚪ WHITE TEAM GRC - Risk Assessment Tool
    
    Evalúa y gestiona riesgos de seguridad con metodología cuantitativa.
    """
    assessor = RiskAssessor(workspace)
    
    if new:
        risk = assessor.create_risk(interactive=interactive)
        file_path = assessor.save_risk(risk)
        console.print(f"\n[green]✓ Risk saved to: {file_path}[/green]")
        assessor.display_risk(risk)
    elif list_risks:
        assessor.generate_register_report()
    elif view:
        assessor.load_risks()
        risk = next((r for r in assessor.risks if r.id == view), None)
        if risk:
            assessor.display_risk(risk)
        else:
            console.print(f"[red]Risk {view} not found[/red]")
    else:
        # Default: show matrix and instructions
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - Risk Assessment Tool[/bold white]",
            border_style="white"
        ))
        console.print(RISK_MATRIX)
        console.print("\n[cyan]Usage:[/cyan]")
        console.print("  --new, -n        Create new risk assessment")
        console.print("  --list, -l       List all risks in register")
        console.print("  --view ID        View specific risk")
        console.print("  --help           Show all options")

if __name__ == '__main__':
    main()
