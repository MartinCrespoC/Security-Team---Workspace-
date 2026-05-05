#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🗺️ MITRE MAPPER - Purple Team Windsurf                                       ║
║  Mapeo y visualización de técnicas MITRE ATT&CK                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python mitre_mapper.py --technique T1003.001
    python mitre_mapper.py --tactic "Credential Access"
    python mitre_mapper.py --coverage-map
    python mitre_mapper.py --export-navigator
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.tree import Tree
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent.parent
MITRE_DIR = BASE_DIR / "mitre"
ATTACKS_DIR = BASE_DIR / "attacks"
DETECTIONS_DIR = BASE_DIR / "detections"
NAVIGATOR_DIR = MITRE_DIR / "navigator"

console = Console() if RICH_AVAILABLE else None

# ═══════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS MITRE ATT&CK
# ═══════════════════════════════════════════════════════════════════════════════

MITRE_TACTICS = {
    "reconnaissance": {
        "id": "TA0043",
        "name": "Reconnaissance",
        "description": "Gathering information to plan future operations"
    },
    "resource-development": {
        "id": "TA0042",
        "name": "Resource Development",
        "description": "Establishing resources to support operations"
    },
    "initial-access": {
        "id": "TA0001",
        "name": "Initial Access",
        "description": "Trying to get into your network"
    },
    "execution": {
        "id": "TA0002",
        "name": "Execution",
        "description": "Trying to run malicious code"
    },
    "persistence": {
        "id": "TA0003",
        "name": "Persistence",
        "description": "Trying to maintain foothold"
    },
    "privilege-escalation": {
        "id": "TA0004",
        "name": "Privilege Escalation",
        "description": "Trying to gain higher-level permissions"
    },
    "defense-evasion": {
        "id": "TA0005",
        "name": "Defense Evasion",
        "description": "Trying to avoid being detected"
    },
    "credential-access": {
        "id": "TA0006",
        "name": "Credential Access",
        "description": "Stealing account names and passwords"
    },
    "discovery": {
        "id": "TA0007",
        "name": "Discovery",
        "description": "Trying to figure out your environment"
    },
    "lateral-movement": {
        "id": "TA0008",
        "name": "Lateral Movement",
        "description": "Moving through your environment"
    },
    "collection": {
        "id": "TA0009",
        "name": "Collection",
        "description": "Gathering data of interest"
    },
    "command-and-control": {
        "id": "TA0011",
        "name": "Command and Control",
        "description": "Communicating with compromised systems"
    },
    "exfiltration": {
        "id": "TA0010",
        "name": "Exfiltration",
        "description": "Stealing data"
    },
    "impact": {
        "id": "TA0040",
        "name": "Impact",
        "description": "Manipulate, interrupt, or destroy systems and data"
    }
}

MITRE_TECHNIQUES = {
    # Credential Access
    "T1003": {
        "name": "OS Credential Dumping",
        "tactic": "credential-access",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Process Monitoring", "PowerShell Logs", "API Monitoring"],
        "subtechniques": {
            "T1003.001": {
                "name": "LSASS Memory",
                "platforms": ["Windows"],
                "detection": "Monitor for unexpected access to LSASS"
            },
            "T1003.002": {
                "name": "Security Account Manager",
                "platforms": ["Windows"],
                "detection": "Monitor for registry access to SAM"
            },
            "T1003.003": {
                "name": "NTDS",
                "platforms": ["Windows"],
                "detection": "Monitor for ntdsutil usage"
            },
            "T1003.004": {
                "name": "LSA Secrets",
                "platforms": ["Windows"],
                "detection": "Monitor for registry access to LSA"
            },
            "T1003.005": {
                "name": "Cached Domain Credentials",
                "platforms": ["Windows"],
                "detection": "Monitor for registry access"
            },
            "T1003.006": {
                "name": "DCSync",
                "platforms": ["Windows"],
                "detection": "Monitor for replication requests"
            },
            "T1003.007": {
                "name": "Proc Filesystem",
                "platforms": ["Linux"],
                "detection": "Monitor /proc access"
            },
            "T1003.008": {
                "name": "/etc/passwd and /etc/shadow",
                "platforms": ["Linux"],
                "detection": "Monitor file access"
            }
        }
    },
    # Execution
    "T1059": {
        "name": "Command and Scripting Interpreter",
        "tactic": "execution",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Process Monitoring", "Command-Line Logging"],
        "subtechniques": {
            "T1059.001": {
                "name": "PowerShell",
                "platforms": ["Windows"],
                "detection": "Script Block Logging, Module Logging"
            },
            "T1059.003": {
                "name": "Windows Command Shell",
                "platforms": ["Windows"],
                "detection": "Command-line logging"
            },
            "T1059.004": {
                "name": "Unix Shell",
                "platforms": ["Linux", "macOS"],
                "detection": "Auditd, bash history"
            },
            "T1059.005": {
                "name": "Visual Basic",
                "platforms": ["Windows"],
                "detection": "Process monitoring"
            },
            "T1059.006": {
                "name": "Python",
                "platforms": ["Windows", "Linux", "macOS"],
                "detection": "Process monitoring"
            },
            "T1059.007": {
                "name": "JavaScript",
                "platforms": ["Windows", "Linux", "macOS"],
                "detection": "Process monitoring"
            }
        }
    },
    # Persistence
    "T1547": {
        "name": "Boot or Logon Autostart Execution",
        "tactic": "persistence",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Registry Monitoring", "File Monitoring"],
        "subtechniques": {
            "T1547.001": {
                "name": "Registry Run Keys / Startup Folder",
                "platforms": ["Windows"],
                "detection": "Registry monitoring"
            },
            "T1547.004": {
                "name": "Winlogon Helper DLL",
                "platforms": ["Windows"],
                "detection": "Registry monitoring"
            },
            "T1547.009": {
                "name": "Shortcut Modification",
                "platforms": ["Windows"],
                "detection": "File monitoring"
            }
        }
    },
    # Defense Evasion
    "T1055": {
        "name": "Process Injection",
        "tactic": "defense-evasion",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["API Monitoring", "Process Monitoring"],
        "subtechniques": {
            "T1055.001": {
                "name": "Dynamic-link Library Injection",
                "platforms": ["Windows"],
                "detection": "API monitoring, Sysmon"
            },
            "T1055.002": {
                "name": "Portable Executable Injection",
                "platforms": ["Windows"],
                "detection": "Memory analysis"
            },
            "T1055.003": {
                "name": "Thread Execution Hijacking",
                "platforms": ["Windows"],
                "detection": "API monitoring"
            },
            "T1055.004": {
                "name": "Asynchronous Procedure Call",
                "platforms": ["Windows"],
                "detection": "API monitoring"
            },
            "T1055.012": {
                "name": "Process Hollowing",
                "platforms": ["Windows"],
                "detection": "Memory analysis"
            }
        }
    },
    "T1070": {
        "name": "Indicator Removal",
        "tactic": "defense-evasion",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Event Logs", "File Monitoring"],
        "subtechniques": {
            "T1070.001": {
                "name": "Clear Windows Event Logs",
                "platforms": ["Windows"],
                "detection": "Event ID 1102"
            },
            "T1070.002": {
                "name": "Clear Linux or Mac System Logs",
                "platforms": ["Linux", "macOS"],
                "detection": "File monitoring"
            },
            "T1070.003": {
                "name": "Clear Command History",
                "platforms": ["Linux", "macOS", "Windows"],
                "detection": "File monitoring"
            },
            "T1070.004": {
                "name": "File Deletion",
                "platforms": ["Windows", "Linux", "macOS"],
                "detection": "File monitoring"
            }
        }
    },
    # Discovery
    "T1082": {
        "name": "System Information Discovery",
        "tactic": "discovery",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Process Monitoring", "Command-Line Logging"],
        "subtechniques": {}
    },
    "T1083": {
        "name": "File and Directory Discovery",
        "tactic": "discovery",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Process Monitoring", "Command-Line Logging"],
        "subtechniques": {}
    },
    # Lateral Movement
    "T1021": {
        "name": "Remote Services",
        "tactic": "lateral-movement",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Authentication Logs", "Network Traffic"],
        "subtechniques": {
            "T1021.001": {
                "name": "Remote Desktop Protocol",
                "platforms": ["Windows"],
                "detection": "Network monitoring, Event 4624"
            },
            "T1021.002": {
                "name": "SMB/Windows Admin Shares",
                "platforms": ["Windows"],
                "detection": "Network monitoring, Event 5140"
            },
            "T1021.003": {
                "name": "Distributed Component Object Model",
                "platforms": ["Windows"],
                "detection": "Process monitoring"
            },
            "T1021.004": {
                "name": "SSH",
                "platforms": ["Linux", "macOS"],
                "detection": "Authentication logs"
            },
            "T1021.006": {
                "name": "Windows Remote Management",
                "platforms": ["Windows"],
                "detection": "Network monitoring, Event logs"
            }
        }
    },
    # Collection
    "T1005": {
        "name": "Data from Local System",
        "tactic": "collection",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["File Monitoring", "Process Monitoring"],
        "subtechniques": {}
    },
    # Exfiltration
    "T1048": {
        "name": "Exfiltration Over Alternative Protocol",
        "tactic": "exfiltration",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Network Traffic", "Process Monitoring"],
        "subtechniques": {
            "T1048.001": {
                "name": "Exfiltration Over Symmetric Encrypted Non-C2 Protocol",
                "platforms": ["Windows", "Linux", "macOS"],
                "detection": "Network monitoring"
            },
            "T1048.002": {
                "name": "Exfiltration Over Asymmetric Encrypted Non-C2 Protocol",
                "platforms": ["Windows", "Linux", "macOS"],
                "detection": "Network monitoring"
            },
            "T1048.003": {
                "name": "Exfiltration Over Unencrypted Non-C2 Protocol",
                "platforms": ["Windows", "Linux", "macOS"],
                "detection": "Network monitoring, DLP"
            }
        }
    },
    # Impact
    "T1486": {
        "name": "Data Encrypted for Impact",
        "tactic": "impact",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["File Monitoring", "Process Monitoring"],
        "subtechniques": {}
    },
    "T1489": {
        "name": "Service Stop",
        "tactic": "impact",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Process Monitoring", "Service Monitoring"],
        "subtechniques": {}
    },
    "T1490": {
        "name": "Inhibit System Recovery",
        "tactic": "impact",
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": ["Process Monitoring", "Command-Line Logging"],
        "subtechniques": {}
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE MAPEO
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Mostrar banner del script."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  ███╗   ███╗██╗████████╗██████╗ ███████╗    ███╗   ███╗ █████╗ ██████╗       ║
║  ████╗ ████║██║╚══██╔══╝██╔══██╗██╔════╝    ████╗ ████║██╔══██╗██╔══██╗      ║
║  ██╔████╔██║██║   ██║   ██████╔╝█████╗      ██╔████╔██║███████║██████╔╝      ║
║  ██║╚██╔╝██║██║   ██║   ██╔══██╗██╔══╝      ██║╚██╔╝██║██╔══██║██╔═══╝       ║
║  ██║ ╚═╝ ██║██║   ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║  ██║██║           ║
║  ╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝           ║
║                                                                               ║
║  🗺️ MITRE MAPPER - Purple Team Windsurf                                       ║
║  Mapeo y visualización de técnicas ATT&CK                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    if RICH_AVAILABLE:
        console.print(Panel(banner, style="cyan"))
    else:
        print(banner)

def get_technique_info(technique_id: str) -> Optional[Dict]:
    """Obtener información completa de una técnica."""
    base_id = technique_id.split('.')[0]
    
    if base_id not in MITRE_TECHNIQUES:
        return None
    
    technique = MITRE_TECHNIQUES[base_id]
    
    if '.' in technique_id:
        # Es una subtécnica
        if technique_id in technique.get('subtechniques', {}):
            sub = technique['subtechniques'][technique_id]
            return {
                'id': technique_id,
                'name': sub['name'],
                'parent_id': base_id,
                'parent_name': technique['name'],
                'tactic': technique['tactic'],
                'platforms': sub.get('platforms', technique['platforms']),
                'detection': sub.get('detection', ''),
                'data_sources': technique.get('data_sources', [])
            }
    else:
        return {
            'id': technique_id,
            'name': technique['name'],
            'tactic': technique['tactic'],
            'platforms': technique['platforms'],
            'data_sources': technique.get('data_sources', []),
            'subtechniques': list(technique.get('subtechniques', {}).keys())
        }
    
    return None

def display_technique(technique_id: str):
    """Mostrar información detallada de una técnica."""
    info = get_technique_info(technique_id)
    
    if not info:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Técnica {technique_id} no encontrada[/red]")
        else:
            print(f"❌ Técnica {technique_id} no encontrada")
        return
    
    tactic_info = MITRE_TACTICS.get(info['tactic'], {})
    
    if RICH_AVAILABLE:
        console.print(f"\n[bold cyan]{'═' * 70}[/bold cyan]")
        console.print(f"[bold cyan]  🎯 {info['id']} - {info['name']}[/bold cyan]")
        console.print(f"[bold cyan]{'═' * 70}[/bold cyan]")
        
        console.print(f"\n  [yellow]Táctica:[/yellow]      {tactic_info.get('name', info['tactic'])} ({tactic_info.get('id', '')})")
        console.print(f"  [yellow]Plataformas:[/yellow]  {', '.join(info.get('platforms', []))}")
        
        if info.get('data_sources'):
            console.print(f"  [yellow]Data Sources:[/yellow] {', '.join(info['data_sources'])}")
        
        if info.get('detection'):
            console.print(f"  [yellow]Detección:[/yellow]    {info['detection']}")
        
        if info.get('parent_id'):
            console.print(f"\n  [magenta]Técnica Padre:[/magenta] {info['parent_id']} - {info['parent_name']}")
        
        if info.get('subtechniques'):
            console.print(f"\n  [green]Subtécnicas:[/green]")
            for sub_id in info['subtechniques']:
                sub_info = get_technique_info(sub_id)
                if sub_info:
                    console.print(f"    • {sub_id} - {sub_info['name']}")
        
        # Mostrar URL de MITRE
        console.print(f"\n  [blue]🔗 URL:[/blue] https://attack.mitre.org/techniques/{technique_id.replace('.', '/')}/")
    else:
        print(f"\n{'═' * 70}")
        print(f"  🎯 {info['id']} - {info['name']}")
        print(f"{'═' * 70}")
        print(f"\n  Táctica:      {tactic_info.get('name', info['tactic'])}")
        print(f"  Plataformas:  {', '.join(info.get('platforms', []))}")
        
        if info.get('subtechniques'):
            print(f"\n  Subtécnicas:")
            for sub_id in info['subtechniques']:
                sub_info = get_technique_info(sub_id)
                if sub_info:
                    print(f"    • {sub_id} - {sub_info['name']}")

def list_tactics():
    """Listar todas las tácticas."""
    if RICH_AVAILABLE:
        table = Table(title="🎯 Tácticas MITRE ATT&CK")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Descripción", style="white")
        
        for key, tactic in MITRE_TACTICS.items():
            table.add_row(tactic['id'], tactic['name'], tactic['description'])
        
        console.print(table)
    else:
        print("\n🎯 Tácticas MITRE ATT&CK\n")
        print("-" * 80)
        for key, tactic in MITRE_TACTICS.items():
            print(f"{tactic['id']:8} | {tactic['name']:25} | {tactic['description']}")

def list_techniques_by_tactic(tactic: str):
    """Listar técnicas por táctica."""
    tactic_key = tactic.lower().replace(' ', '-')
    
    if RICH_AVAILABLE:
        table = Table(title=f"🎯 Técnicas - {tactic}")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Plataformas", style="yellow")
        table.add_column("Subtécnicas", style="magenta")
        
        for tech_id, tech_info in MITRE_TECHNIQUES.items():
            if tech_info['tactic'] == tactic_key:
                subs = len(tech_info.get('subtechniques', {}))
                table.add_row(
                    tech_id,
                    tech_info['name'],
                    ', '.join(tech_info['platforms']),
                    str(subs) if subs > 0 else "-"
                )
        
        console.print(table)
    else:
        print(f"\n🎯 Técnicas - {tactic}\n")
        print("-" * 80)
        for tech_id, tech_info in MITRE_TECHNIQUES.items():
            if tech_info['tactic'] == tactic_key:
                print(f"{tech_id:10} | {tech_info['name']:40} | {', '.join(tech_info['platforms'])}")

def get_coverage_data() -> Dict[str, Dict]:
    """Obtener datos de cobertura de detección."""
    coverage = {}
    
    for tech_id in MITRE_TECHNIQUES:
        detection_path = DETECTIONS_DIR / tech_id
        attack_path = ATTACKS_DIR / tech_id
        
        has_detection = detection_path.exists() and any(detection_path.glob("*.yaml"))
        has_attack = attack_path.exists() and any(attack_path.glob("*.yaml"))
        
        # Obtener cobertura del último archivo de detección
        cov_percent = 0
        if has_detection:
            yaml_files = list(detection_path.glob("*.yaml"))
            if yaml_files:
                latest = max(yaml_files, key=lambda x: x.stat().st_mtime)
                try:
                    with open(latest) as f:
                        data = yaml.safe_load(f)
                    cov_percent = data.get('coverage', 0)
                except Exception:
                    pass
        
        coverage[tech_id] = {
            'tested': has_attack,
            'detected': has_detection,
            'coverage': cov_percent
        }
        
        # Subtécnicas
        for sub_id in MITRE_TECHNIQUES[tech_id].get('subtechniques', {}):
            sub_detection_path = DETECTIONS_DIR / sub_id
            sub_attack_path = ATTACKS_DIR / sub_id
            
            sub_has_detection = sub_detection_path.exists() and any(sub_detection_path.glob("*.yaml"))
            sub_has_attack = sub_attack_path.exists() and any(sub_attack_path.glob("*.yaml"))
            
            sub_cov = 0
            if sub_has_detection:
                yaml_files = list(sub_detection_path.glob("*.yaml"))
                if yaml_files:
                    latest = max(yaml_files, key=lambda x: x.stat().st_mtime)
                    try:
                        with open(latest) as f:
                            data = yaml.safe_load(f)
                        sub_cov = data.get('coverage', 0)
                    except Exception:
                        pass
            
            coverage[sub_id] = {
                'tested': sub_has_attack,
                'detected': sub_has_detection,
                'coverage': sub_cov
            }
    
    return coverage

def display_coverage_map():
    """Mostrar mapa de cobertura."""
    coverage = get_coverage_data()
    
    if RICH_AVAILABLE:
        console.print("\n[bold purple]" + "═" * 70 + "[/bold purple]")
        console.print("[bold purple]  📊 MAPA DE COBERTURA ATT&CK[/bold purple]")
        console.print("[bold purple]" + "═" * 70 + "[/bold purple]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Técnica", style="white")
        table.add_column("Nombre", style="white")
        table.add_column("Probada", justify="center")
        table.add_column("Detectada", justify="center")
        table.add_column("Cobertura", justify="right")
        table.add_column("Estado", justify="center")
        
        for tech_id, tech_info in MITRE_TECHNIQUES.items():
            cov = coverage.get(tech_id, {})
            
            tested = "✅" if cov.get('tested') else "❌"
            detected = "✅" if cov.get('detected') else "❌"
            cov_percent = cov.get('coverage', 0)
            
            if cov_percent >= 80:
                status = "[green]●[/green]"
                cov_str = f"[green]{cov_percent}%[/green]"
            elif cov_percent >= 50:
                status = "[yellow]●[/yellow]"
                cov_str = f"[yellow]{cov_percent}%[/yellow]"
            elif cov_percent > 0:
                status = "[orange1]●[/orange1]"
                cov_str = f"[orange1]{cov_percent}%[/orange1]"
            else:
                status = "[red]●[/red]"
                cov_str = f"[red]{cov_percent}%[/red]"
            
            table.add_row(tech_id, tech_info['name'], tested, detected, cov_str, status)
        
        console.print(table)
        
        # Resumen
        total = len(coverage)
        tested = sum(1 for c in coverage.values() if c.get('tested'))
        detected = sum(1 for c in coverage.values() if c.get('detected'))
        avg_coverage = sum(c.get('coverage', 0) for c in coverage.values()) / total if total > 0 else 0
        
        console.print(f"\n[cyan]📈 Resumen:[/cyan]")
        console.print(f"   Total técnicas: {total}")
        console.print(f"   Probadas: {tested} ({tested*100//total}%)")
        console.print(f"   Con detección: {detected} ({detected*100//total}%)")
        console.print(f"   Cobertura promedio: {avg_coverage:.1f}%")
    else:
        print("\n" + "═" * 70)
        print("  📊 MAPA DE COBERTURA ATT&CK")
        print("═" * 70)
        
        for tech_id, tech_info in MITRE_TECHNIQUES.items():
            cov = coverage.get(tech_id, {})
            tested = "✅" if cov.get('tested') else "❌"
            detected = "✅" if cov.get('detected') else "❌"
            cov_percent = cov.get('coverage', 0)
            print(f"{tech_id:10} | {tech_info['name']:35} | {tested} | {detected} | {cov_percent}%")

def export_navigator_layer():
    """Exportar capa para ATT&CK Navigator."""
    coverage = get_coverage_data()
    
    techniques = []
    for tech_id, cov in coverage.items():
        cov_percent = cov.get('coverage', 0)
        
        # Determinar color basado en cobertura
        if cov_percent >= 80:
            color = "#00ff00"  # Verde
            score = 100
        elif cov_percent >= 50:
            color = "#ffff00"  # Amarillo
            score = 75
        elif cov_percent > 0:
            color = "#ff8000"  # Naranja
            score = 50
        else:
            color = "#ff0000"  # Rojo
            score = 0
        
        techniques.append({
            "techniqueID": tech_id,
            "color": color,
            "score": score,
            "comment": f"Coverage: {cov_percent}%",
            "enabled": True
        })
    
    layer = {
        "name": "Purple Team Coverage",
        "versions": {
            "attack": "14",
            "navigator": "4.9.1",
            "layer": "4.5"
        },
        "domain": "enterprise-attack",
        "description": f"Purple Team detection coverage map - Generated {datetime.now().isoformat()}",
        "filters": {
            "platforms": ["Windows", "Linux", "macOS"]
        },
        "sorting": 0,
        "layout": {
            "layout": "side",
            "aggregateFunction": "average",
            "showID": True,
            "showName": True
        },
        "hideDisabled": False,
        "techniques": techniques,
        "gradient": {
            "colors": ["#ff0000", "#ff8000", "#ffff00", "#00ff00"],
            "minValue": 0,
            "maxValue": 100
        },
        "legendItems": [
            {"label": "No Coverage (0%)", "color": "#ff0000"},
            {"label": "Low Coverage (1-49%)", "color": "#ff8000"},
            {"label": "Medium Coverage (50-79%)", "color": "#ffff00"},
            {"label": "High Coverage (80-100%)", "color": "#00ff00"}
        ],
        "metadata": [],
        "showTacticRowBackground": True,
        "tacticRowBackground": "#dddddd",
        "selectTechniquesAcrossTactics": True,
        "selectSubtechniquesWithParent": False
    }
    
    # Guardar archivo
    NAVIGATOR_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"purple_team_coverage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = NAVIGATOR_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(layer, f, indent=2)
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Capa Navigator exportada:[/green] {filepath}")
        console.print(f"[cyan]   Abrir en:[/cyan] https://mitre-attack.github.io/attack-navigator/")
    else:
        print(f"\n✅ Capa Navigator exportada: {filepath}")
        print("   Abrir en: https://mitre-attack.github.io/attack-navigator/")
    
    return filepath

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🗺️ MITRE Mapper - Purple Team Windsurf",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-t', '--technique',
        help='Mostrar información de técnica específica'
    )
    parser.add_argument(
        '--tactic',
        help='Listar técnicas por táctica'
    )
    parser.add_argument(
        '--list-tactics',
        action='store_true',
        help='Listar todas las tácticas'
    )
    parser.add_argument(
        '-c', '--coverage-map',
        action='store_true',
        help='Mostrar mapa de cobertura'
    )
    parser.add_argument(
        '-e', '--export-navigator',
        action='store_true',
        help='Exportar capa para ATT&CK Navigator'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo de salida'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.technique:
        display_technique(args.technique)
    elif args.list_tactics:
        list_tactics()
    elif args.tactic:
        list_techniques_by_tactic(args.tactic)
    elif args.coverage_map:
        display_coverage_map()
    elif args.export_navigator:
        export_navigator_layer()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
