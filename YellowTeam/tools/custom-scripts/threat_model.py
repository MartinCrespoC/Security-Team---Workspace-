#!/usr/bin/env python3
"""
🟡 YELLOW TEAM - Threat Model Generator
Generates comprehensive threat models using STRIDE methodology
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    import typer
except ImportError:
    print("Installing required packages...")
    os.system("pip install rich typer")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    import typer

console = Console()
app = typer.Typer(help="🟡 Yellow Team Threat Model Generator")

# STRIDE Categories
STRIDE = {
    "S": {
        "name": "Spoofing",
        "icon": "🎭",
        "description": "Pretending to be someone or something else",
        "property": "Authentication",
        "examples": [
            "Credential theft",
            "Session hijacking",
            "Token forgery",
            "Man-in-the-middle",
        ],
        "mitigations": [
            "Multi-factor authentication",
            "Strong session management",
            "Certificate pinning",
            "Mutual TLS",
        ],
    },
    "T": {
        "name": "Tampering",
        "icon": "✏️",
        "description": "Modifying data or code",
        "property": "Integrity",
        "examples": [
            "SQL injection",
            "Parameter manipulation",
            "Code injection",
            "Data modification",
        ],
        "mitigations": [
            "Input validation",
            "Digital signatures",
            "Integrity checks",
            "Immutable audit logs",
        ],
    },
    "R": {
        "name": "Repudiation",
        "icon": "🚫",
        "description": "Denying having performed an action",
        "property": "Non-repudiation",
        "examples": [
            "Deleting logs",
            "Denying transactions",
            "Timestamp manipulation",
            "Identity spoofing",
        ],
        "mitigations": [
            "Audit logging",
            "Digital signatures",
            "Timestamps",
            "Secure log storage",
        ],
    },
    "I": {
        "name": "Information Disclosure",
        "icon": "📤",
        "description": "Exposing information to unauthorized parties",
        "property": "Confidentiality",
        "examples": [
            "Data breach",
            "Error message leakage",
            "Side-channel attacks",
            "Insecure storage",
        ],
        "mitigations": [
            "Encryption",
            "Access control",
            "Data masking",
            "Secure error handling",
        ],
    },
    "D": {
        "name": "Denial of Service",
        "icon": "💥",
        "description": "Denying or degrading service to users",
        "property": "Availability",
        "examples": [
            "Resource exhaustion",
            "DDoS attacks",
            "Application crashes",
            "Storage filling",
        ],
        "mitigations": [
            "Rate limiting",
            "Resource quotas",
            "Redundancy",
            "Auto-scaling",
        ],
    },
    "E": {
        "name": "Elevation of Privilege",
        "icon": "⬆️",
        "description": "Gaining capabilities without authorization",
        "property": "Authorization",
        "examples": [
            "Privilege escalation",
            "IDOR vulnerabilities",
            "Role manipulation",
            "Sandbox escape",
        ],
        "mitigations": [
            "Least privilege",
            "RBAC/ABAC",
            "Sandboxing",
            "Regular audits",
        ],
    },
}


class ThreatModel:
    """Threat Model data structure"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.version = "1.0"
        self.created = datetime.now().isoformat()
        self.author = os.getenv("USER", "Yellow Team")
        self.components = []
        self.data_flows = []
        self.trust_boundaries = []
        self.threats = []
        self.mitigations = []

    def add_component(self, name: str, type_: str, description: str = ""):
        """Add a system component"""
        self.components.append(
            {"name": name, "type": type_, "description": description}
        )

    def add_data_flow(
        self, source: str, destination: str, data_type: str, protocol: str = ""
    ):
        """Add a data flow"""
        self.data_flows.append(
            {
                "source": source,
                "destination": destination,
                "data_type": data_type,
                "protocol": protocol,
            }
        )

    def add_trust_boundary(self, name: str, components: list):
        """Add a trust boundary"""
        self.trust_boundaries.append({"name": name, "components": components})

    def add_threat(
        self,
        stride_category: str,
        title: str,
        description: str,
        component: str,
        impact: str = "Medium",
        likelihood: str = "Medium",
    ):
        """Add an identified threat"""
        risk_matrix = {
            ("High", "High"): "Critical",
            ("High", "Medium"): "High",
            ("High", "Low"): "Medium",
            ("Medium", "High"): "High",
            ("Medium", "Medium"): "Medium",
            ("Medium", "Low"): "Low",
            ("Low", "High"): "Medium",
            ("Low", "Medium"): "Low",
            ("Low", "Low"): "Low",
        }

        risk = risk_matrix.get((impact, likelihood), "Medium")

        self.threats.append(
            {
                "id": f"{stride_category}-{len([t for t in self.threats if t['category'] == stride_category]) + 1:03d}",
                "category": stride_category,
                "title": title,
                "description": description,
                "component": component,
                "impact": impact,
                "likelihood": likelihood,
                "risk": risk,
            }
        )

    def add_mitigation(self, threat_id: str, control: str, status: str = "Proposed"):
        """Add a mitigation for a threat"""
        self.mitigations.append(
            {"threat_id": threat_id, "control": control, "status": status}
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "created": self.created,
            "author": self.author,
            "components": self.components,
            "data_flows": self.data_flows,
            "trust_boundaries": self.trust_boundaries,
            "threats": self.threats,
            "mitigations": self.mitigations,
        }

    def to_markdown(self) -> str:
        """Generate Markdown report"""
        md = f"""# 🟡 Threat Model: {self.name}

## Document Information
| Field | Value |
|-------|-------|
| **System** | {self.name} |
| **Version** | {self.version} |
| **Created** | {self.created} |
| **Author** | {self.author} |

## System Description
{self.description}

## Components

| Component | Type | Description |
|-----------|------|-------------|
"""
        for comp in self.components:
            md += f"| {comp['name']} | {comp['type']} | {comp['description']} |\n"

        md += """
## Data Flow Diagram

```mermaid
flowchart LR
"""
        # Add trust boundaries
        for i, tb in enumerate(self.trust_boundaries):
            md += f"    subgraph TB{i}[{tb['name']}]\n"
            for comp in tb["components"]:
                md += f"        {comp.replace(' ', '_')}[{comp}]\n"
            md += "    end\n"

        # Add data flows
        for flow in self.data_flows:
            src = flow["source"].replace(" ", "_")
            dst = flow["destination"].replace(" ", "_")
            label = flow["data_type"]
            md += f"    {src} -->|{label}| {dst}\n"

        md += "```\n\n"

        md += "## STRIDE Threat Analysis\n\n"

        for category, info in STRIDE.items():
            category_threats = [t for t in self.threats if t["category"] == category]
            md += f"### {info['icon']} {info['name']} ({info['property']})\n\n"

            if category_threats:
                md += "| ID | Threat | Component | Impact | Likelihood | Risk |\n"
                md += "|----|--------|-----------|--------|------------|------|\n"
                for threat in category_threats:
                    md += f"| {threat['id']} | {threat['title']} | {threat['component']} | {threat['impact']} | {threat['likelihood']} | **{threat['risk']}** |\n"
            else:
                md += "*No threats identified in this category*\n"
            md += "\n"

        md += "## Risk Summary\n\n"

        risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for threat in self.threats:
            risk_counts[threat["risk"]] += 1

        md += "| Risk Level | Count |\n"
        md += "|------------|-------|\n"
        for level, count in risk_counts.items():
            emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}[level]
            md += f"| {emoji} {level} | {count} |\n"

        md += "\n## Mitigations\n\n"
        md += "| Threat ID | Control | Status |\n"
        md += "|-----------|---------|--------|\n"
        for mit in self.mitigations:
            md += f"| {mit['threat_id']} | {mit['control']} | {mit['status']} |\n"

        md += """
## Recommendations

Based on the threat analysis, the following actions are recommended:

1. **Critical/High Risk Threats**: Address immediately before deployment
2. **Medium Risk Threats**: Include in security backlog for near-term remediation
3. **Low Risk Threats**: Monitor and address as resources permit

## Appendix

### STRIDE Reference

| Category | Property | Description |
|----------|----------|-------------|
"""
        for cat, info in STRIDE.items():
            md += f"| {info['icon']} {info['name']} | {info['property']} | {info['description']} |\n"

        md += f"""
---
*Generated by Yellow Team Threat Model Generator*
*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return md


def print_banner():
    """Print Yellow Team banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🟡 YELLOW TEAM - THREAT MODEL GENERATOR                                     ║
║                                                                               ║
║   Security Architecture & Threat Modeling                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    console.print(Panel(banner, style="yellow"))


def interactive_mode():
    """Run interactive threat modeling session"""
    print_banner()

    console.print("\n[bold yellow]📋 System Information[/bold yellow]\n")

    name = Prompt.ask("System name")
    description = Prompt.ask("System description")

    model = ThreatModel(name, description)

    # Components
    console.print("\n[bold yellow]🧩 Components[/bold yellow]")
    console.print("Add system components (type 'done' when finished)\n")

    while True:
        comp_name = Prompt.ask("Component name (or 'done')")
        if comp_name.lower() == "done":
            break
        comp_type = Prompt.ask(
            "Component type",
            choices=["Web App", "API", "Database", "Service", "External", "User"],
        )
        comp_desc = Prompt.ask("Description", default="")
        model.add_component(comp_name, comp_type, comp_desc)

    # Data Flows
    console.print("\n[bold yellow]🔄 Data Flows[/bold yellow]")
    console.print("Add data flows (type 'done' when finished)\n")

    while True:
        source = Prompt.ask("Source (or 'done')")
        if source.lower() == "done":
            break
        dest = Prompt.ask("Destination")
        data_type = Prompt.ask("Data type")
        protocol = Prompt.ask("Protocol", default="HTTPS")
        model.add_data_flow(source, dest, data_type, protocol)

    # Trust Boundaries
    console.print("\n[bold yellow]🛡️ Trust Boundaries[/bold yellow]")
    console.print("Add trust boundaries (type 'done' when finished)\n")

    while True:
        tb_name = Prompt.ask("Trust boundary name (or 'done')")
        if tb_name.lower() == "done":
            break
        components_str = Prompt.ask("Components (comma-separated)")
        components = [c.strip() for c in components_str.split(",")]
        model.add_trust_boundary(tb_name, components)

    # STRIDE Analysis
    console.print("\n[bold yellow]⚔️ STRIDE Threat Analysis[/bold yellow]\n")

    for category, info in STRIDE.items():
        console.print(f"\n[bold]{info['icon']} {info['name']}[/bold]")
        console.print(f"Property: {info['property']}")
        console.print(f"Examples: {', '.join(info['examples'][:2])}")

        if Confirm.ask(f"Add threats for {info['name']}?"):
            while True:
                title = Prompt.ask("Threat title (or 'done')")
                if title.lower() == "done":
                    break
                desc = Prompt.ask("Description")
                component = Prompt.ask("Affected component")
                impact = Prompt.ask("Impact", choices=["High", "Medium", "Low"])
                likelihood = Prompt.ask("Likelihood", choices=["High", "Medium", "Low"])

                model.add_threat(category, title, desc, component, impact, likelihood)

                # Suggest mitigation
                console.print(f"\nSuggested mitigations: {', '.join(info['mitigations'])}")
                mitigation = Prompt.ask("Mitigation control")
                model.add_mitigation(model.threats[-1]["id"], mitigation)

    # Generate output
    console.print("\n[bold yellow]📄 Generating Threat Model...[/bold yellow]\n")

    # Save files
    script_dir = Path(__file__).parent.parent.parent
    output_dir = script_dir / "threat-models"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = name.lower().replace(" ", "-")

    # Save Markdown
    md_file = output_dir / f"{safe_name}-threat-model-{timestamp}.md"
    with open(md_file, "w") as f:
        f.write(model.to_markdown())
    console.print(f"[green]✓[/green] Markdown saved: {md_file}")

    # Save JSON
    json_file = output_dir / f"{safe_name}-threat-model-{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(model.to_dict(), f, indent=2)
    console.print(f"[green]✓[/green] JSON saved: {json_file}")

    # Display summary
    console.print("\n[bold yellow]📊 Summary[/bold yellow]\n")

    table = Table(title="Threat Model Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="yellow")

    table.add_row("Components", str(len(model.components)))
    table.add_row("Data Flows", str(len(model.data_flows)))
    table.add_row("Trust Boundaries", str(len(model.trust_boundaries)))
    table.add_row("Threats Identified", str(len(model.threats)))
    table.add_row("Mitigations", str(len(model.mitigations)))

    console.print(table)

    # Risk breakdown
    risk_table = Table(title="Risk Breakdown")
    risk_table.add_column("Risk Level", style="cyan")
    risk_table.add_column("Count", style="yellow")

    risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for threat in model.threats:
        risk_counts[threat["risk"]] += 1

    for level, count in risk_counts.items():
        emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}[level]
        risk_table.add_row(f"{emoji} {level}", str(count))

    console.print(risk_table)


@app.command()
def create(
    name: str = typer.Option(None, "--name", "-n", help="System name"),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactive mode"
    ),
    output: str = typer.Option(None, "--output", "-o", help="Output directory"),
):
    """Create a new threat model"""
    if interactive or not name:
        interactive_mode()
    else:
        console.print(f"Creating threat model for: {name}")
        model = ThreatModel(name)
        console.print("[yellow]Use --interactive for guided threat modeling[/yellow]")


@app.command()
def analyze(
    file: str = typer.Argument(..., help="Architecture file to analyze"),
):
    """Analyze an architecture file for threats"""
    console.print(f"[yellow]Analyzing: {file}[/yellow]")
    # TODO: Implement file analysis
    console.print("[yellow]File analysis coming soon...[/yellow]")


@app.command()
def template(
    output: str = typer.Option(".", "--output", "-o", help="Output directory"),
):
    """Generate a threat model template"""
    template_content = """# Threat Model Template

## System Information
- **System Name:**
- **Version:**
- **Date:**
- **Author:**

## System Description
[Describe the system here]

## Components
| Component | Type | Description |
|-----------|------|-------------|
| | | |

## Data Flow Diagram
```mermaid
flowchart LR
    User[User] --> WebApp[Web Application]
    WebApp --> API[API Server]
    API --> DB[(Database)]
```

## STRIDE Analysis

### 🎭 Spoofing
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| S-001 | | | | |

### ✏️ Tampering
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| T-001 | | | | |

### 🚫 Repudiation
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| R-001 | | | | |

### 📤 Information Disclosure
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| I-001 | | | | |

### 💥 Denial of Service
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| D-001 | | | | |

### ⬆️ Elevation of Privilege
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| E-001 | | | | |

## Risk Summary
| Risk Level | Count |
|------------|-------|
| 🔴 Critical | |
| 🟠 High | |
| 🟡 Medium | |
| 🟢 Low | |

## Recommendations
1.
2.
3.
"""
    output_path = Path(output) / "threat-model-template.md"
    with open(output_path, "w") as f:
        f.write(template_content)
    console.print(f"[green]✓[/green] Template saved: {output_path}")


if __name__ == "__main__":
    app()
