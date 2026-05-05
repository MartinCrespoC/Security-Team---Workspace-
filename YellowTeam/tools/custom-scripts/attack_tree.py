#!/usr/bin/env python3
"""
🟡 YELLOW TEAM - Attack Tree Generator
Generates attack trees for threat modeling
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, field

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.tree import Tree
    import typer
except ImportError:
    print("Installing required packages...")
    os.system("pip install rich typer")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.tree import Tree
    import typer

console = Console()
app = typer.Typer(help="🟡 Yellow Team Attack Tree Generator")


@dataclass
class AttackNode:
    """Represents a node in the attack tree"""
    id: str
    name: str
    description: str = ""
    node_type: str = "OR"  # OR, AND
    likelihood: str = "Medium"  # High, Medium, Low
    impact: str = "Medium"  # High, Medium, Low
    cost: str = "Medium"  # High, Medium, Low (attacker cost)
    skill: str = "Medium"  # High, Medium, Low (required skill)
    mitigations: List[str] = field(default_factory=list)
    children: List["AttackNode"] = field(default_factory=list)

    def add_child(self, child: "AttackNode"):
        """Add a child node"""
        self.children.append(child)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "node_type": self.node_type,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "cost": self.cost,
            "skill": self.skill,
            "mitigations": self.mitigations,
            "children": [child.to_dict() for child in self.children]
        }

    def calculate_risk(self) -> str:
        """Calculate risk based on likelihood and impact"""
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
        return risk_matrix.get((self.likelihood, self.impact), "Medium")


class AttackTree:
    """Attack Tree data structure"""

    def __init__(self, name: str, target: str, description: str = ""):
        self.name = name
        self.target = target
        self.description = description
        self.created = datetime.now().isoformat()
        self.author = os.getenv("USER", "Yellow Team")
        self.root: Optional[AttackNode] = None
        self.node_counter = 0

    def create_node(self, name: str, description: str = "",
                    node_type: str = "OR", likelihood: str = "Medium",
                    impact: str = "Medium", cost: str = "Medium",
                    skill: str = "Medium") -> AttackNode:
        """Create a new attack node"""
        self.node_counter += 1
        node_id = f"ATK-{self.node_counter:03d}"
        return AttackNode(
            id=node_id,
            name=name,
            description=description,
            node_type=node_type,
            likelihood=likelihood,
            impact=impact,
            cost=cost,
            skill=skill
        )

    def set_root(self, node: AttackNode):
        """Set the root node (attack goal)"""
        self.root = node

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "target": self.target,
            "description": self.description,
            "created": self.created,
            "author": self.author,
            "root": self.root.to_dict() if self.root else None
        }

    def _node_to_mermaid(self, node: AttackNode, parent_id: str = None) -> str:
        """Convert node to Mermaid syntax"""
        lines = []

        # Node shape based on type
        if node.node_type == "AND":
            shape = f"{node.id}[/{node.name}/]"
        else:
            shape = f"{node.id}[{node.name}]"

        if parent_id:
            lines.append(f"    {parent_id} --> {shape}")
        else:
            lines.append(f"    {shape}")

        for child in node.children:
            lines.extend(self._node_to_mermaid(child, node.id).split("\n"))

        return "\n".join(lines)

    def to_mermaid(self) -> str:
        """Generate Mermaid diagram"""
        if not self.root:
            return "graph TD\n    empty[No attack tree defined]"

        mermaid = "graph TD\n"
        mermaid += self._node_to_mermaid(self.root)

        # Add styling
        mermaid += "\n\n    %% Styling\n"
        mermaid += "    classDef goal fill:#ff6b6b,stroke:#c92a2a,color:#fff\n"
        mermaid += "    classDef high fill:#ffa94d,stroke:#e8590c,color:#000\n"
        mermaid += "    classDef medium fill:#ffd43b,stroke:#f59f00,color:#000\n"
        mermaid += "    classDef low fill:#69db7c,stroke:#2f9e44,color:#000\n"

        if self.root:
            mermaid += f"    class {self.root.id} goal\n"

        return mermaid

    def _node_to_markdown_tree(self, node: AttackNode, level: int = 0) -> str:
        """Convert node to markdown tree format"""
        indent = "  " * level
        risk = node.calculate_risk()
        risk_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(risk, "⚪")

        type_indicator = "[AND]" if node.node_type == "AND" else "[OR]"

        line = f"{indent}- **{node.id}** {node.name} {type_indicator} {risk_emoji}\n"

        if node.description:
            line += f"{indent}  - *{node.description}*\n"

        if node.mitigations:
            line += f"{indent}  - Mitigations: {', '.join(node.mitigations)}\n"

        for child in node.children:
            line += self._node_to_markdown_tree(child, level + 1)

        return line

    def to_markdown(self) -> str:
        """Generate Markdown report"""
        md = f"""# 🟡 Attack Tree: {self.name}

## Overview

| Field | Value |
|-------|-------|
| **Target** | {self.target} |
| **Created** | {self.created} |
| **Author** | {self.author} |

## Description
{self.description}

## Attack Tree Diagram

```mermaid
{self.to_mermaid()}
```

## Attack Tree Structure

"""
        if self.root:
            md += self._node_to_markdown_tree(self.root)
        else:
            md += "*No attack tree defined*\n"

        md += """
## Attack Paths Analysis

"""
        if self.root:
            md += self._analyze_paths(self.root)

        md += """
## Legend

| Symbol | Meaning |
|--------|---------|
| [OR] | Any child path achieves the goal |
| [AND] | All child paths required |
| 🔴 | Critical Risk |
| 🟠 | High Risk |
| 🟡 | Medium Risk |
| 🟢 | Low Risk |

## Recommendations

Based on the attack tree analysis:

1. **Focus on high-likelihood, high-impact paths first**
2. **Implement defense in depth** - multiple controls per path
3. **Monitor for attack indicators** along identified paths
4. **Regular review** - update tree as system evolves

---
*Generated by Yellow Team Attack Tree Generator*
*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return md

    def _analyze_paths(self, node: AttackNode, path: List[str] = None) -> str:
        """Analyze attack paths"""
        if path is None:
            path = []

        current_path = path + [node.name]
        analysis = ""

        if not node.children:
            # Leaf node - this is an attack technique
            risk = node.calculate_risk()
            analysis += f"### Path: {' → '.join(current_path)}\n\n"
            analysis += f"- **Risk**: {risk}\n"
            analysis += f"- **Likelihood**: {node.likelihood}\n"
            analysis += f"- **Impact**: {node.impact}\n"
            analysis += f"- **Attacker Cost**: {node.cost}\n"
            analysis += f"- **Required Skill**: {node.skill}\n"
            if node.mitigations:
                analysis += f"- **Mitigations**: {', '.join(node.mitigations)}\n"
            analysis += "\n"
        else:
            for child in node.children:
                analysis += self._analyze_paths(child, current_path)

        return analysis


def print_banner():
    """Print Yellow Team banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🟡 YELLOW TEAM - ATTACK TREE GENERATOR                                      ║
║                                                                               ║
║   Model Attack Paths & Identify Mitigations                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    console.print(Panel(banner, style="yellow"))


def build_node_interactive(tree: AttackTree, parent_name: str = "root") -> Optional[AttackNode]:
    """Interactively build an attack node"""
    console.print(f"\n[bold yellow]Adding node under: {parent_name}[/bold yellow]")

    name = Prompt.ask("Attack step/goal name (or 'done' to finish)")
    if name.lower() == "done":
        return None

    description = Prompt.ask("Description", default="")
    node_type = Prompt.ask("Node type", choices=["OR", "AND"], default="OR")
    likelihood = Prompt.ask("Likelihood", choices=["High", "Medium", "Low"], default="Medium")
    impact = Prompt.ask("Impact", choices=["High", "Medium", "Low"], default="Medium")
    cost = Prompt.ask("Attacker cost", choices=["High", "Medium", "Low"], default="Medium")
    skill = Prompt.ask("Required skill", choices=["High", "Medium", "Low"], default="Medium")

    node = tree.create_node(
        name=name,
        description=description,
        node_type=node_type,
        likelihood=likelihood,
        impact=impact,
        cost=cost,
        skill=skill
    )

    # Add mitigations
    if Confirm.ask("Add mitigations?"):
        while True:
            mitigation = Prompt.ask("Mitigation (or 'done')")
            if mitigation.lower() == "done":
                break
            node.mitigations.append(mitigation)

    # Add children
    if Confirm.ask("Add child nodes (sub-attacks)?"):
        while True:
            child = build_node_interactive(tree, name)
            if child is None:
                break
            node.add_child(child)

    return node


def interactive_mode():
    """Run interactive attack tree building"""
    print_banner()

    console.print("\n[bold yellow]📋 Attack Tree Information[/bold yellow]\n")

    name = Prompt.ask("Attack tree name")
    target = Prompt.ask("Target system/asset")
    description = Prompt.ask("Description", default="")

    tree = AttackTree(name, target, description)

    console.print("\n[bold yellow]🎯 Define Attack Goal (Root Node)[/bold yellow]")
    console.print("The root node represents the attacker's ultimate goal.\n")

    root = build_node_interactive(tree, "Attack Goal")
    if root:
        tree.set_root(root)

    # Generate output
    console.print("\n[bold yellow]📄 Generating Attack Tree...[/bold yellow]\n")

    script_dir = Path(__file__).parent.parent.parent
    output_dir = script_dir / "threat-models"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = name.lower().replace(" ", "-")

    # Save Markdown
    md_file = output_dir / f"{safe_name}-attack-tree-{timestamp}.md"
    with open(md_file, "w") as f:
        f.write(tree.to_markdown())
    console.print(f"[green]✓[/green] Markdown saved: {md_file}")

    # Save JSON
    json_file = output_dir / f"{safe_name}-attack-tree-{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(tree.to_dict(), f, indent=2)
    console.print(f"[green]✓[/green] JSON saved: {json_file}")

    # Display tree
    if tree.root:
        console.print("\n[bold yellow]🌳 Attack Tree Preview[/bold yellow]\n")
        rich_tree = Tree(f"🎯 {tree.root.name}")
        _build_rich_tree(rich_tree, tree.root)
        console.print(rich_tree)


def _build_rich_tree(rich_tree: Tree, node: AttackNode):
    """Build Rich tree for display"""
    for child in node.children:
        risk = child.calculate_risk()
        risk_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(risk, "⚪")
        type_str = "[AND]" if child.node_type == "AND" else "[OR]"
        branch = rich_tree.add(f"{risk_emoji} {child.name} {type_str}")
        _build_rich_tree(branch, child)


@app.command()
def create(
    name: str = typer.Option(None, "--name", "-n", help="Attack tree name"),
    target: str = typer.Option(None, "--target", "-t", help="Target system"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
):
    """Create a new attack tree"""
    if interactive or not name:
        interactive_mode()
    else:
        console.print(f"Creating attack tree: {name}")
        console.print("[yellow]Use --interactive for guided creation[/yellow]")


@app.command()
def template(
    output: str = typer.Option(".", "--output", "-o", help="Output directory"),
):
    """Generate attack tree template"""
    template_content = """# Attack Tree Template

## Overview
| Field | Value |
|-------|-------|
| **Target** | [System/Asset] |
| **Goal** | [Attacker's Goal] |
| **Date** | [Date] |

## Attack Tree

```mermaid
graph TD
    Goal[🎯 Compromise System]

    Goal --> A[Exploit Vulnerability]
    Goal --> B[Social Engineering]
    Goal --> C[Insider Threat]

    A --> A1[SQL Injection]
    A --> A2[XSS Attack]

    B --> B1[Phishing]
    B --> B2[Pretexting]

    C --> C1[Malicious Admin]
    C --> C2[Compromised Credentials]

    classDef goal fill:#ff6b6b,stroke:#c92a2a,color:#fff
    class Goal goal
```

## Attack Paths

### Path 1: SQL Injection
- **Likelihood**: Medium
- **Impact**: High
- **Risk**: High
- **Mitigations**: Input validation, parameterized queries, WAF

### Path 2: Phishing
- **Likelihood**: High
- **Impact**: Medium
- **Risk**: High
- **Mitigations**: Security awareness, email filtering, MFA

## Legend
| Symbol | Meaning |
|--------|---------|
| [OR] | Any child achieves goal |
| [AND] | All children required |
| 🔴 | Critical |
| 🟠 | High |
| 🟡 | Medium |
| 🟢 | Low |
"""
    output_path = Path(output) / "attack-tree-template.md"
    with open(output_path, "w") as f:
        f.write(template_content)
    console.print(f"[green]✓[/green] Template saved: {output_path}")


@app.command()
def examples():
    """Show attack tree examples"""
    print_banner()

    console.print("\n[bold yellow]Common Attack Tree Patterns[/bold yellow]\n")

    examples_data = [
        {
            "goal": "Compromise User Account",
            "paths": ["Credential Theft", "Social Engineering", "Session Hijacking"]
        },
        {
            "goal": "Data Exfiltration",
            "paths": ["SQL Injection", "API Abuse", "Insider Access"]
        },
        {
            "goal": "Denial of Service",
            "paths": ["Resource Exhaustion", "Application Crash", "Network Flood"]
        },
        {
            "goal": "Privilege Escalation",
            "paths": ["Exploit Vulnerability", "Misconfiguration", "Token Manipulation"]
        }
    ]

    for example in examples_data:
        tree = Tree(f"🎯 {example['goal']}")
        for path in example["paths"]:
            tree.add(f"📍 {path}")
        console.print(tree)
        console.print()


if __name__ == "__main__":
    app()
