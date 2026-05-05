#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🟣 GAP ANALYZER - Purple Team Windsurf                                       ║
║  Analizador de brechas de detección                                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python gap_analyzer.py --technique T1003.001
    python gap_analyzer.py --tactic "Credential Access"
    python gap_analyzer.py --full-analysis
    python gap_analyzer.py --generate-recommendations
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.tree import Tree
    from rich.progress import Progress
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent.parent
GAPS_DIR = BASE_DIR / "gaps"
ATTACKS_DIR = BASE_DIR / "attacks"
DETECTIONS_DIR = BASE_DIR / "detections"
RULES_DIR = BASE_DIR / "rules"
RECOMMENDATIONS_DIR = GAPS_DIR / "recommendations"

console = Console() if RICH_AVAILABLE else None

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS Y DATACLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class GapType(Enum):
    NO_DETECTION = "no_detection"
    PARTIAL_DETECTION = "partial_detection"
    DELAYED_DETECTION = "delayed_detection"
    HIGH_FALSE_POSITIVES = "high_false_positives"
    NO_RULE = "no_rule"
    RULE_NOT_ENABLED = "rule_not_enabled"

@dataclass
class Gap:
    technique_id: str
    technique_name: str
    tactic: str
    gap_type: GapType
    severity: Severity
    description: str
    current_coverage: int
    expected_coverage: int
    detection_sources_missing: List[str]
    recommendations: List[str]
    sigma_rule_suggestion: Optional[str] = None
    yara_rule_suggestion: Optional[str] = None
    priority_score: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'technique_id': self.technique_id,
            'technique_name': self.technique_name,
            'tactic': self.tactic,
            'gap_type': self.gap_type.value,
            'severity': self.severity.value,
            'description': self.description,
            'current_coverage': self.current_coverage,
            'expected_coverage': self.expected_coverage,
            'detection_sources_missing': self.detection_sources_missing,
            'recommendations': self.recommendations,
            'sigma_rule_suggestion': self.sigma_rule_suggestion,
            'yara_rule_suggestion': self.yara_rule_suggestion,
            'priority_score': self.priority_score
        }

@dataclass
class AnalysisResult:
    timestamp: str
    total_techniques: int
    techniques_with_gaps: int
    critical_gaps: int
    high_gaps: int
    medium_gaps: int
    low_gaps: int
    overall_coverage: float
    gaps: List[Gap] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'total_techniques': self.total_techniques,
            'techniques_with_gaps': self.techniques_with_gaps,
            'critical_gaps': self.critical_gaps,
            'high_gaps': self.high_gaps,
            'medium_gaps': self.medium_gaps,
            'low_gaps': self.low_gaps,
            'overall_coverage': self.overall_coverage,
            'gaps': [g.to_dict() for g in self.gaps]
        }

# ═══════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS DE TÉCNICAS Y DETECCIONES ESPERADAS
# ═══════════════════════════════════════════════════════════════════════════════

TECHNIQUE_DETECTION_REQUIREMENTS = {
    "T1003.001": {
        "name": "LSASS Memory",
        "tactic": "Credential Access",
        "severity": Severity.CRITICAL,
        "expected_coverage": 90,
        "required_sources": ["sysmon", "edr", "sigma"],
        "sigma_rule": """
title: LSASS Memory Access
status: experimental
logsource:
    category: process_access
    product: windows
detection:
    selection:
        TargetImage|endswith: '\\lsass.exe'
        GrantedAccess|contains:
            - '0x1010'
            - '0x1038'
            - '0x1438'
            - '0x143a'
    filter:
        SourceImage|endswith:
            - '\\wmiprvse.exe'
            - '\\taskmgr.exe'
    condition: selection and not filter
falsepositives:
    - Legitimate administrative tools
level: high
tags:
    - attack.credential_access
    - attack.t1003.001
"""
    },
    "T1059.001": {
        "name": "PowerShell",
        "tactic": "Execution",
        "severity": Severity.HIGH,
        "expected_coverage": 85,
        "required_sources": ["powershell", "sysmon", "sigma"],
        "sigma_rule": """
title: Suspicious PowerShell Execution
status: experimental
logsource:
    product: windows
    category: ps_script
detection:
    selection:
        ScriptBlockText|contains:
            - 'IEX'
            - 'Invoke-Expression'
            - 'DownloadString'
            - 'Net.WebClient'
            - '-enc'
            - '-EncodedCommand'
    condition: selection
falsepositives:
    - Legitimate administrative scripts
level: medium
tags:
    - attack.execution
    - attack.t1059.001
"""
    },
    "T1547.001": {
        "name": "Registry Run Keys",
        "tactic": "Persistence",
        "severity": Severity.HIGH,
        "expected_coverage": 85,
        "required_sources": ["sysmon", "windows_security", "sigma"],
        "sigma_rule": """
title: Registry Run Key Modification
status: experimental
logsource:
    category: registry_set
    product: windows
detection:
    selection:
        TargetObject|contains:
            - '\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
            - '\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce'
    condition: selection
falsepositives:
    - Legitimate software installation
level: medium
tags:
    - attack.persistence
    - attack.t1547.001
"""
    },
    "T1055.001": {
        "name": "DLL Injection",
        "tactic": "Defense Evasion",
        "severity": Severity.CRITICAL,
        "expected_coverage": 80,
        "required_sources": ["sysmon", "edr", "sigma"],
        "sigma_rule": """
title: CreateRemoteThread API Call
status: experimental
logsource:
    category: create_remote_thread
    product: windows
detection:
    selection:
        EventType: CreateRemoteThread
    filter:
        SourceImage|endswith:
            - '\\csrss.exe'
            - '\\wininit.exe'
    condition: selection and not filter
falsepositives:
    - Legitimate remote thread creation
level: high
tags:
    - attack.defense_evasion
    - attack.t1055.001
"""
    },
    "T1070.001": {
        "name": "Clear Windows Event Logs",
        "tactic": "Defense Evasion",
        "severity": Severity.HIGH,
        "expected_coverage": 95,
        "required_sources": ["windows_security", "sysmon", "sigma"],
        "sigma_rule": """
title: Security Event Log Cleared
status: stable
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 1102
    condition: selection
falsepositives:
    - Legitimate log maintenance
level: high
tags:
    - attack.defense_evasion
    - attack.t1070.001
"""
    },
    "T1021.002": {
        "name": "SMB/Windows Admin Shares",
        "tactic": "Lateral Movement",
        "severity": Severity.HIGH,
        "expected_coverage": 80,
        "required_sources": ["network", "windows_security", "sigma"],
        "sigma_rule": """
title: Admin Share Access
status: experimental
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 5140
        ShareName|contains:
            - 'ADMIN$'
            - 'C$'
            - 'IPC$'
    condition: selection
falsepositives:
    - Legitimate administrative access
level: medium
tags:
    - attack.lateral_movement
    - attack.t1021.002
"""
    },
    "T1486": {
        "name": "Data Encrypted for Impact",
        "tactic": "Impact",
        "severity": Severity.CRITICAL,
        "expected_coverage": 90,
        "required_sources": ["edr", "sysmon", "sigma", "yara"],
        "sigma_rule": """
title: Ransomware File Modification Pattern
status: experimental
logsource:
    category: file_event
    product: windows
detection:
    selection:
        TargetFilename|endswith:
            - '.encrypted'
            - '.locked'
            - '.crypto'
    condition: selection
falsepositives:
    - Legitimate encryption software
level: critical
tags:
    - attack.impact
    - attack.t1486
"""
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE ANÁLISIS
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Mostrar banner del script."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗  █████╗ ██████╗      █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗      ║
║  ██╔════╝ ██╔══██╗██╔══██╗    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝      ║
║  ██║  ███╗███████║██████╔╝    ███████║██╔██╗ ██║███████║██║   ╚████╔╝       ║
║  ██║   ██║██╔══██║██╔═══╝     ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝        ║
║  ╚██████╔╝██║  ██║██║         ██║  ██║██║ ╚████║██║  ██║███████╗██║         ║
║   ╚═════╝ ╚═╝  ╚═╝╚═╝         ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝         ║
║                                                                               ║
║  🟣 GAP ANALYZER - Purple Team Windsurf                                       ║
║  Analizador de brechas de detección                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    if RICH_AVAILABLE:
        console.print(Panel(banner, style="purple"))
    else:
        print(banner)

def get_current_coverage(technique_id: str) -> Tuple[int, List[str]]:
    """Obtener cobertura actual de una técnica."""
    detection_path = DETECTIONS_DIR / technique_id
    
    if not detection_path.exists():
        return 0, []
    
    # Buscar último archivo de validación
    yaml_files = list(detection_path.glob("*.yaml"))
    if not yaml_files:
        return 0, []
    
    latest_file = max(yaml_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file) as f:
            data = yaml.safe_load(f)
        
        coverage = data.get('coverage', 0)
        detected_sources = []
        
        for source in data.get('detection_sources', []):
            if source.get('detected', False):
                detected_sources.append(source.get('source', ''))
        
        return coverage, detected_sources
    except Exception:
        return 0, []

def analyze_technique(technique_id: str) -> Optional[Gap]:
    """Analizar una técnica específica para identificar brechas."""
    
    if technique_id not in TECHNIQUE_DETECTION_REQUIREMENTS:
        return None
    
    req = TECHNIQUE_DETECTION_REQUIREMENTS[technique_id]
    current_coverage, detected_sources = get_current_coverage(technique_id)
    expected_coverage = req['expected_coverage']
    
    # Identificar fuentes faltantes
    missing_sources = [s for s in req['required_sources'] if s not in detected_sources]
    
    # Determinar tipo de brecha
    if current_coverage == 0:
        gap_type = GapType.NO_DETECTION
    elif current_coverage < expected_coverage * 0.5:
        gap_type = GapType.PARTIAL_DETECTION
    elif len(missing_sources) > 0:
        gap_type = GapType.NO_RULE
    else:
        return None  # No hay brecha significativa
    
    # Calcular puntuación de prioridad
    severity_scores = {
        Severity.CRITICAL: 100,
        Severity.HIGH: 75,
        Severity.MEDIUM: 50,
        Severity.LOW: 25,
        Severity.INFO: 10
    }
    
    priority_score = severity_scores[req['severity']]
    priority_score += (expected_coverage - current_coverage)
    priority_score += len(missing_sources) * 10
    
    # Generar recomendaciones
    recommendations = []
    
    if 'sigma' in missing_sources:
        recommendations.append(f"Implementar regla Sigma para {technique_id}")
    if 'sysmon' in missing_sources:
        recommendations.append("Habilitar logging de Sysmon para eventos relevantes")
    if 'edr' in missing_sources:
        recommendations.append("Configurar alertas en EDR para esta técnica")
    if 'windows_security' in missing_sources:
        recommendations.append("Habilitar auditoría de Windows Security Events")
    if 'network' in missing_sources:
        recommendations.append("Implementar monitoreo de tráfico de red")
    
    if current_coverage < 50:
        recommendations.append("Priorizar implementación inmediata de detecciones")
    
    return Gap(
        technique_id=technique_id,
        technique_name=req['name'],
        tactic=req['tactic'],
        gap_type=gap_type,
        severity=req['severity'],
        description=f"Cobertura de detección insuficiente para {req['name']}",
        current_coverage=current_coverage,
        expected_coverage=expected_coverage,
        detection_sources_missing=missing_sources,
        recommendations=recommendations,
        sigma_rule_suggestion=req.get('sigma_rule'),
        priority_score=priority_score
    )

def full_analysis() -> AnalysisResult:
    """Realizar análisis completo de todas las técnicas."""
    
    gaps = []
    total_coverage = 0
    
    for technique_id in TECHNIQUE_DETECTION_REQUIREMENTS:
        gap = analyze_technique(technique_id)
        if gap:
            gaps.append(gap)
        
        coverage, _ = get_current_coverage(technique_id)
        total_coverage += coverage
    
    # Ordenar por prioridad
    gaps.sort(key=lambda x: x.priority_score, reverse=True)
    
    # Contar por severidad
    critical = sum(1 for g in gaps if g.severity == Severity.CRITICAL)
    high = sum(1 for g in gaps if g.severity == Severity.HIGH)
    medium = sum(1 for g in gaps if g.severity == Severity.MEDIUM)
    low = sum(1 for g in gaps if g.severity == Severity.LOW)
    
    total_techniques = len(TECHNIQUE_DETECTION_REQUIREMENTS)
    overall_coverage = total_coverage / total_techniques if total_techniques > 0 else 0
    
    return AnalysisResult(
        timestamp=datetime.now().isoformat(),
        total_techniques=total_techniques,
        techniques_with_gaps=len(gaps),
        critical_gaps=critical,
        high_gaps=high,
        medium_gaps=medium,
        low_gaps=low,
        overall_coverage=overall_coverage,
        gaps=gaps
    )

def display_gap(gap: Gap):
    """Mostrar información de una brecha."""
    
    severity_colors = {
        Severity.CRITICAL: "red",
        Severity.HIGH: "orange1",
        Severity.MEDIUM: "yellow",
        Severity.LOW: "blue",
        Severity.INFO: "white"
    }
    
    if RICH_AVAILABLE:
        color = severity_colors.get(gap.severity, "white")
        
        console.print(f"\n[bold {color}]{'═' * 70}[/bold {color}]")
        console.print(f"[bold {color}]  🔍 BRECHA: {gap.technique_id} - {gap.technique_name}[/bold {color}]")
        console.print(f"[bold {color}]{'═' * 70}[/bold {color}]")
        
        console.print(f"\n  [cyan]Táctica:[/cyan]          {gap.tactic}")
        console.print(f"  [cyan]Severidad:[/cyan]        [{color}]{gap.severity.value.upper()}[/{color}]")
        console.print(f"  [cyan]Tipo de Brecha:[/cyan]   {gap.gap_type.value}")
        console.print(f"  [cyan]Cobertura Actual:[/cyan] {gap.current_coverage}%")
        console.print(f"  [cyan]Cobertura Esperada:[/cyan] {gap.expected_coverage}%")
        console.print(f"  [cyan]Prioridad:[/cyan]        {gap.priority_score}")
        
        if gap.detection_sources_missing:
            console.print(f"\n  [yellow]⚠️  Fuentes de Detección Faltantes:[/yellow]")
            for source in gap.detection_sources_missing:
                console.print(f"      • {source}")
        
        if gap.recommendations:
            console.print(f"\n  [green]📋 Recomendaciones:[/green]")
            for i, rec in enumerate(gap.recommendations, 1):
                console.print(f"      {i}. {rec}")
        
        if gap.sigma_rule_suggestion:
            console.print(f"\n  [magenta]📜 Regla Sigma Sugerida:[/magenta]")
            console.print(Panel(gap.sigma_rule_suggestion, title="Sigma Rule", border_style="magenta"))
    else:
        print(f"\n{'═' * 70}")
        print(f"  🔍 BRECHA: {gap.technique_id} - {gap.technique_name}")
        print(f"{'═' * 70}")
        print(f"\n  Táctica:          {gap.tactic}")
        print(f"  Severidad:        {gap.severity.value.upper()}")
        print(f"  Tipo de Brecha:   {gap.gap_type.value}")
        print(f"  Cobertura Actual: {gap.current_coverage}%")
        print(f"  Cobertura Esperada: {gap.expected_coverage}%")
        
        if gap.detection_sources_missing:
            print(f"\n  ⚠️  Fuentes de Detección Faltantes:")
            for source in gap.detection_sources_missing:
                print(f"      • {source}")
        
        if gap.recommendations:
            print(f"\n  📋 Recomendaciones:")
            for i, rec in enumerate(gap.recommendations, 1):
                print(f"      {i}. {rec}")

def display_analysis_summary(result: AnalysisResult):
    """Mostrar resumen del análisis."""
    
    if RICH_AVAILABLE:
        console.print("\n[bold purple]" + "═" * 70 + "[/bold purple]")
        console.print("[bold purple]  📊 RESUMEN DE ANÁLISIS DE BRECHAS[/bold purple]")
        console.print("[bold purple]" + "═" * 70 + "[/bold purple]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Métrica", style="white")
        table.add_column("Valor", justify="right")
        
        table.add_row("Total Técnicas Analizadas", str(result.total_techniques))
        table.add_row("Técnicas con Brechas", str(result.techniques_with_gaps))
        table.add_row("Brechas Críticas", f"[red]{result.critical_gaps}[/red]")
        table.add_row("Brechas Altas", f"[orange1]{result.high_gaps}[/orange1]")
        table.add_row("Brechas Medias", f"[yellow]{result.medium_gaps}[/yellow]")
        table.add_row("Brechas Bajas", f"[blue]{result.low_gaps}[/blue]")
        table.add_row("Cobertura General", f"{result.overall_coverage:.1f}%")
        
        console.print(table)
        
        # Indicador visual
        coverage = result.overall_coverage
        if coverage >= 80:
            console.print(f"\n  [green]{'█' * 20}[/green] [green]EXCELENTE[/green]")
        elif coverage >= 60:
            console.print(f"\n  [yellow]{'█' * 16}{'░' * 4}[/yellow] [yellow]BUENO[/yellow]")
        elif coverage >= 40:
            console.print(f"\n  [yellow]{'█' * 12}{'░' * 8}[/yellow] [yellow]REGULAR[/yellow]")
        else:
            console.print(f"\n  [red]{'█' * 8}{'░' * 12}[/red] [red]DEFICIENTE[/red]")
    else:
        print(f"\n{'═' * 70}")
        print("  📊 RESUMEN DE ANÁLISIS DE BRECHAS")
        print(f"{'═' * 70}")
        print(f"\n  Total Técnicas Analizadas: {result.total_techniques}")
        print(f"  Técnicas con Brechas:      {result.techniques_with_gaps}")
        print(f"  Brechas Críticas:          {result.critical_gaps}")
        print(f"  Brechas Altas:             {result.high_gaps}")
        print(f"  Brechas Medias:            {result.medium_gaps}")
        print(f"  Brechas Bajas:             {result.low_gaps}")
        print(f"  Cobertura General:         {result.overall_coverage:.1f}%")

def save_analysis(result: AnalysisResult):
    """Guardar resultado del análisis."""
    
    # Crear directorio
    GAPS_DIR.mkdir(parents=True, exist_ok=True)
    analysis_dir = GAPS_DIR / "analysis"
    analysis_dir.mkdir(exist_ok=True)
    
    # Guardar YAML
    filename = f"gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    filepath = analysis_dir / filename
    
    with open(filepath, 'w') as f:
        yaml.dump(result.to_dict(), f, default_flow_style=False, allow_unicode=True)
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Análisis guardado en:[/green] {filepath}")
    else:
        print(f"\n✅ Análisis guardado en: {filepath}")

def generate_recommendations_report(result: AnalysisResult):
    """Generar reporte de recomendaciones."""
    
    RECOMMENDATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    filename = f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = RECOMMENDATIONS_DIR / filename
    
    with open(filepath, 'w') as f:
        f.write("# 🟣 Purple Team - Recomendaciones de Mejora\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Cobertura General:** {result.overall_coverage:.1f}%\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 Resumen\n\n")
        f.write(f"- Total Técnicas: {result.total_techniques}\n")
        f.write(f"- Brechas Críticas: {result.critical_gaps}\n")
        f.write(f"- Brechas Altas: {result.high_gaps}\n")
        f.write(f"- Brechas Medias: {result.medium_gaps}\n")
        f.write(f"- Brechas Bajas: {result.low_gaps}\n\n")
        
        f.write("---\n\n")
        f.write("## 🔴 Brechas Críticas (Acción Inmediata)\n\n")
        
        for gap in result.gaps:
            if gap.severity == Severity.CRITICAL:
                f.write(f"### {gap.technique_id} - {gap.technique_name}\n\n")
                f.write(f"- **Táctica:** {gap.tactic}\n")
                f.write(f"- **Cobertura:** {gap.current_coverage}% / {gap.expected_coverage}%\n")
                f.write(f"- **Fuentes Faltantes:** {', '.join(gap.detection_sources_missing)}\n\n")
                f.write("**Recomendaciones:**\n")
                for rec in gap.recommendations:
                    f.write(f"- {rec}\n")
                f.write("\n")
                
                if gap.sigma_rule_suggestion:
                    f.write("**Regla Sigma Sugerida:**\n")
                    f.write(f"```yaml\n{gap.sigma_rule_suggestion}\n```\n\n")
        
        f.write("---\n\n")
        f.write("## 🟠 Brechas Altas\n\n")
        
        for gap in result.gaps:
            if gap.severity == Severity.HIGH:
                f.write(f"### {gap.technique_id} - {gap.technique_name}\n\n")
                f.write(f"- **Táctica:** {gap.tactic}\n")
                f.write(f"- **Cobertura:** {gap.current_coverage}% / {gap.expected_coverage}%\n\n")
                f.write("**Recomendaciones:**\n")
                for rec in gap.recommendations:
                    f.write(f"- {rec}\n")
                f.write("\n")
        
        f.write("---\n\n")
        f.write("## 📋 Plan de Acción\n\n")
        f.write("| Prioridad | Técnica | Acción | Responsable | Fecha Límite |\n")
        f.write("|-----------|---------|--------|-------------|-------------|\n")
        
        for i, gap in enumerate(result.gaps[:10], 1):
            f.write(f"| {i} | {gap.technique_id} | {gap.recommendations[0] if gap.recommendations else 'Revisar'} | Blue Team | TBD |\n")
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Reporte de recomendaciones guardado en:[/green] {filepath}")
    else:
        print(f"\n✅ Reporte de recomendaciones guardado en: {filepath}")

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🟣 Gap Analyzer - Purple Team Windsurf",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-t', '--technique',
        help='Analizar técnica específica (ej: T1003.001)'
    )
    parser.add_argument(
        '--tactic',
        help='Filtrar por táctica ATT&CK'
    )
    parser.add_argument(
        '-f', '--full-analysis',
        action='store_true',
        help='Realizar análisis completo'
    )
    parser.add_argument(
        '-r', '--generate-recommendations',
        action='store_true',
        help='Generar reporte de recomendaciones'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo de salida'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Salida detallada'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.technique:
        gap = analyze_technique(args.technique)
        if gap:
            display_gap(gap)
            
            # Guardar gap individual
            gap_dir = GAPS_DIR / args.technique
            gap_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"gap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            with open(gap_dir / filename, 'w') as f:
                yaml.dump(gap.to_dict(), f, default_flow_style=False, allow_unicode=True)
        else:
            if RICH_AVAILABLE:
                console.print(f"\n[green]✅ No se encontraron brechas significativas para {args.technique}[/green]")
            else:
                print(f"\n✅ No se encontraron brechas significativas para {args.technique}")
    
    elif args.full_analysis or args.generate_recommendations:
        result = full_analysis()
        display_analysis_summary(result)
        
        if args.verbose:
            for gap in result.gaps:
                display_gap(gap)
        
        save_analysis(result)
        
        if args.generate_recommendations:
            generate_recommendations_report(result)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
