#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  📊 PURPLE REPORT - Purple Team Windsurf                                      ║
║  Generador de reportes de ejercicios Purple Team                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python purple_report.py --exercise-report
    python purple_report.py --gap-report
    python purple_report.py --metrics-report
    python purple_report.py --executive-summary
    python purple_report.py --full-report
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import hashlib

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from jinja2 import Template
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent.parent
REPORTS_DIR = BASE_DIR / "reports"
ATTACKS_DIR = BASE_DIR / "attacks"
DETECTIONS_DIR = BASE_DIR / "detections"
GAPS_DIR = BASE_DIR / "gaps"
TEMPLATES_DIR = BASE_DIR / "templates"

console = Console() if RICH_AVAILABLE else None

# ═══════════════════════════════════════════════════════════════════════════════
# DATACLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ExerciseMetrics:
    total_techniques_tested: int = 0
    techniques_detected: int = 0
    techniques_not_detected: int = 0
    average_coverage: float = 0.0
    average_mttd: float = 0.0  # Mean Time to Detect (minutes)
    critical_gaps: int = 0
    high_gaps: int = 0
    medium_gaps: int = 0
    low_gaps: int = 0
    false_positive_rate: float = 0.0
    
@dataclass
class TechniqueResult:
    technique_id: str
    technique_name: str
    tactic: str
    tested: bool = False
    detected: bool = False
    coverage: int = 0
    time_to_detect: Optional[float] = None
    detection_sources: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE RECOLECCIÓN DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Mostrar banner del script."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗     ███████╗                           ║
║  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██║     ██╔════╝                           ║
║  ██████╔╝██║   ██║██████╔╝██████╔╝██║     █████╗                             ║
║  ██╔═══╝ ██║   ██║██╔══██╗██╔═══╝ ██║     ██╔══╝                             ║
║  ██║     ╚██████╔╝██║  ██║██║     ███████╗███████╗                           ║
║  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝                           ║
║                                                                               ║
║  ██████╗ ███████╗██████╗  ██████╗ ██████╗ ████████╗                          ║
║  ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝                          ║
║  ██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝   ██║                             ║
║  ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══██╗   ██║                             ║
║  ██║  ██║███████╗██║     ╚██████╔╝██║  ██║   ██║                             ║
║  ╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝                             ║
║                                                                               ║
║  📊 PURPLE REPORT - Generador de Reportes                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    if RICH_AVAILABLE:
        console.print(Panel(banner, style="purple"))
    else:
        print(banner)

def collect_attack_data() -> List[Dict]:
    """Recolectar datos de ataques ejecutados."""
    attacks = []
    
    if not ATTACKS_DIR.exists():
        return attacks
    
    for tech_dir in ATTACKS_DIR.iterdir():
        if tech_dir.is_dir():
            for yaml_file in tech_dir.glob("*.yaml"):
                try:
                    with open(yaml_file) as f:
                        data = yaml.safe_load(f)
                    if data:
                        data['file'] = str(yaml_file)
                        attacks.append(data)
                except Exception:
                    pass
    
    return attacks

def collect_detection_data() -> List[Dict]:
    """Recolectar datos de detecciones."""
    detections = []
    
    if not DETECTIONS_DIR.exists():
        return detections
    
    for tech_dir in DETECTIONS_DIR.iterdir():
        if tech_dir.is_dir():
            for yaml_file in tech_dir.glob("*.yaml"):
                try:
                    with open(yaml_file) as f:
                        data = yaml.safe_load(f)
                    if data:
                        data['file'] = str(yaml_file)
                        detections.append(data)
                except Exception:
                    pass
    
    return detections

def collect_gap_data() -> List[Dict]:
    """Recolectar datos de brechas."""
    gaps = []
    
    if not GAPS_DIR.exists():
        return gaps
    
    for item in GAPS_DIR.rglob("*.yaml"):
        try:
            with open(item) as f:
                data = yaml.safe_load(f)
            if data:
                data['file'] = str(item)
                gaps.append(data)
        except Exception:
            pass
    
    return gaps

def calculate_metrics() -> ExerciseMetrics:
    """Calcular métricas del ejercicio."""
    attacks = collect_attack_data()
    detections = collect_detection_data()
    gaps = collect_gap_data()
    
    metrics = ExerciseMetrics()
    
    # Técnicas probadas
    tested_techniques = set()
    for attack in attacks:
        tech_id = attack.get('technique_id')
        if tech_id:
            tested_techniques.add(tech_id)
    
    metrics.total_techniques_tested = len(tested_techniques)
    
    # Técnicas detectadas y cobertura
    detected_techniques = set()
    total_coverage = 0
    coverage_count = 0
    
    for detection in detections:
        tech_id = detection.get('technique_id')
        coverage = detection.get('coverage', 0)
        
        if tech_id:
            if coverage > 0:
                detected_techniques.add(tech_id)
            total_coverage += coverage
            coverage_count += 1
    
    metrics.techniques_detected = len(detected_techniques)
    metrics.techniques_not_detected = metrics.total_techniques_tested - metrics.techniques_detected
    metrics.average_coverage = total_coverage / coverage_count if coverage_count > 0 else 0
    
    # Brechas por severidad
    for gap in gaps:
        severity = gap.get('severity', '').lower()
        if severity == 'critical':
            metrics.critical_gaps += 1
        elif severity == 'high':
            metrics.high_gaps += 1
        elif severity == 'medium':
            metrics.medium_gaps += 1
        elif severity == 'low':
            metrics.low_gaps += 1
    
    return metrics

def get_technique_results() -> List[TechniqueResult]:
    """Obtener resultados por técnica."""
    attacks = collect_attack_data()
    detections = collect_detection_data()
    gaps = collect_gap_data()
    
    results = {}
    
    # Procesar ataques
    for attack in attacks:
        tech_id = attack.get('technique_id')
        if tech_id:
            if tech_id not in results:
                results[tech_id] = TechniqueResult(
                    technique_id=tech_id,
                    technique_name=attack.get('technique_name', 'Unknown'),
                    tactic=attack.get('tactic', 'Unknown')
                )
            results[tech_id].tested = True
    
    # Procesar detecciones
    for detection in detections:
        tech_id = detection.get('technique_id')
        if tech_id:
            if tech_id not in results:
                results[tech_id] = TechniqueResult(
                    technique_id=tech_id,
                    technique_name='Unknown',
                    tactic='Unknown'
                )
            
            results[tech_id].coverage = detection.get('coverage', 0)
            results[tech_id].detected = results[tech_id].coverage > 0
            
            sources = detection.get('detection_sources', [])
            for source in sources:
                if source.get('detected'):
                    results[tech_id].detection_sources.append(source.get('source', ''))
    
    # Procesar gaps
    for gap in gaps:
        tech_id = gap.get('technique_id')
        if tech_id and tech_id in results:
            results[tech_id].gaps.append(gap.get('gap_type', ''))
            results[tech_id].recommendations.extend(gap.get('recommendations', []))
    
    return list(results.values())

# ═══════════════════════════════════════════════════════════════════════════════
# GENERADORES DE REPORTES
# ═══════════════════════════════════════════════════════════════════════════════

def generate_exercise_report(output_file: Optional[str] = None) -> str:
    """Generar reporte de ejercicio."""
    metrics = calculate_metrics()
    results = get_technique_results()
    
    report_lines = []
    report_lines.append("# 🟣 Purple Team Exercise Report\n")
    report_lines.append(f"**Fecha de Generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("---\n")
    
    # Resumen Ejecutivo
    report_lines.append("## 📋 Resumen Ejecutivo\n")
    report_lines.append(f"- **Técnicas Probadas:** {metrics.total_techniques_tested}")
    report_lines.append(f"- **Técnicas Detectadas:** {metrics.techniques_detected}")
    report_lines.append(f"- **Técnicas No Detectadas:** {metrics.techniques_not_detected}")
    report_lines.append(f"- **Cobertura Promedio:** {metrics.average_coverage:.1f}%")
    report_lines.append(f"- **Brechas Críticas:** {metrics.critical_gaps}")
    report_lines.append(f"- **Brechas Altas:** {metrics.high_gaps}\n")
    
    # Indicador visual
    if metrics.average_coverage >= 80:
        report_lines.append("### Estado General: 🟢 EXCELENTE\n")
    elif metrics.average_coverage >= 60:
        report_lines.append("### Estado General: 🟡 BUENO\n")
    elif metrics.average_coverage >= 40:
        report_lines.append("### Estado General: 🟠 REGULAR\n")
    else:
        report_lines.append("### Estado General: 🔴 DEFICIENTE\n")
    
    report_lines.append("---\n")
    
    # Resultados por Técnica
    report_lines.append("## 🎯 Resultados por Técnica\n")
    report_lines.append("| Técnica | Nombre | Táctica | Probada | Detectada | Cobertura |")
    report_lines.append("|---------|--------|---------|---------|-----------|-----------|")
    
    for result in sorted(results, key=lambda x: x.technique_id):
        tested = "✅" if result.tested else "❌"
        detected = "✅" if result.detected else "❌"
        report_lines.append(
            f"| {result.technique_id} | {result.technique_name[:30]} | {result.tactic} | {tested} | {detected} | {result.coverage}% |"
        )
    
    report_lines.append("\n---\n")
    
    # Técnicas con Brechas
    report_lines.append("## ⚠️ Técnicas con Brechas\n")
    
    gap_results = [r for r in results if r.gaps or r.coverage < 50]
    if gap_results:
        for result in gap_results:
            report_lines.append(f"### {result.technique_id} - {result.technique_name}\n")
            report_lines.append(f"- **Cobertura:** {result.coverage}%")
            if result.gaps:
                report_lines.append(f"- **Tipo de Brecha:** {', '.join(result.gaps)}")
            if result.recommendations:
                report_lines.append("- **Recomendaciones:**")
                for rec in result.recommendations[:3]:
                    report_lines.append(f"  - {rec}")
            report_lines.append("")
    else:
        report_lines.append("No se identificaron brechas significativas.\n")
    
    report_lines.append("---\n")
    
    # Plan de Acción
    report_lines.append("## 📋 Plan de Acción\n")
    report_lines.append("| Prioridad | Técnica | Acción Requerida | Estado |")
    report_lines.append("|-----------|---------|------------------|--------|")
    
    priority = 1
    for result in sorted(gap_results, key=lambda x: x.coverage):
        if priority <= 10:
            action = result.recommendations[0] if result.recommendations else "Implementar detección"
            report_lines.append(f"| {priority} | {result.technique_id} | {action[:50]} | Pendiente |")
            priority += 1
    
    report_lines.append("\n---\n")
    
    # Próximos Pasos
    report_lines.append("## 🚀 Próximos Pasos\n")
    report_lines.append("1. Implementar reglas de detección para técnicas críticas")
    report_lines.append("2. Validar correcciones con re-ejecución de ataques")
    report_lines.append("3. Actualizar playbooks de respuesta")
    report_lines.append("4. Programar siguiente ejercicio Purple Team")
    report_lines.append("5. Revisar métricas de mejora continua\n")
    
    report_content = "\n".join(report_lines)
    
    # Guardar reporte
    if output_file:
        filepath = Path(output_file)
    else:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        exercises_dir = REPORTS_DIR / "exercises"
        exercises_dir.mkdir(exist_ok=True)
        filepath = exercises_dir / f"exercise_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filepath, 'w') as f:
        f.write(report_content)
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Reporte generado:[/green] {filepath}")
    else:
        print(f"\n✅ Reporte generado: {filepath}")
    
    return str(filepath)

def generate_gap_report(output_file: Optional[str] = None) -> str:
    """Generar reporte de brechas."""
    gaps = collect_gap_data()
    
    report_lines = []
    report_lines.append("# 🔍 Gap Analysis Report\n")
    report_lines.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("---\n")
    
    # Resumen
    critical = sum(1 for g in gaps if g.get('severity', '').lower() == 'critical')
    high = sum(1 for g in gaps if g.get('severity', '').lower() == 'high')
    medium = sum(1 for g in gaps if g.get('severity', '').lower() == 'medium')
    low = sum(1 for g in gaps if g.get('severity', '').lower() == 'low')
    
    report_lines.append("## 📊 Resumen de Brechas\n")
    report_lines.append(f"- 🔴 **Críticas:** {critical}")
    report_lines.append(f"- 🟠 **Altas:** {high}")
    report_lines.append(f"- 🟡 **Medias:** {medium}")
    report_lines.append(f"- 🔵 **Bajas:** {low}")
    report_lines.append(f"- **Total:** {len(gaps)}\n")
    
    report_lines.append("---\n")
    
    # Brechas Críticas
    report_lines.append("## 🔴 Brechas Críticas\n")
    critical_gaps = [g for g in gaps if g.get('severity', '').lower() == 'critical']
    
    if critical_gaps:
        for gap in critical_gaps:
            report_lines.append(f"### {gap.get('technique_id', 'N/A')} - {gap.get('technique_name', 'Unknown')}\n")
            report_lines.append(f"- **Tipo:** {gap.get('gap_type', 'N/A')}")
            report_lines.append(f"- **Cobertura Actual:** {gap.get('current_coverage', 0)}%")
            report_lines.append(f"- **Cobertura Esperada:** {gap.get('expected_coverage', 0)}%")
            
            missing = gap.get('detection_sources_missing', [])
            if missing:
                report_lines.append(f"- **Fuentes Faltantes:** {', '.join(missing)}")
            
            recs = gap.get('recommendations', [])
            if recs:
                report_lines.append("- **Recomendaciones:**")
                for rec in recs:
                    report_lines.append(f"  - {rec}")
            
            report_lines.append("")
    else:
        report_lines.append("No hay brechas críticas identificadas.\n")
    
    report_lines.append("---\n")
    
    # Brechas Altas
    report_lines.append("## 🟠 Brechas Altas\n")
    high_gaps = [g for g in gaps if g.get('severity', '').lower() == 'high']
    
    if high_gaps:
        for gap in high_gaps:
            report_lines.append(f"### {gap.get('technique_id', 'N/A')} - {gap.get('technique_name', 'Unknown')}\n")
            report_lines.append(f"- **Cobertura:** {gap.get('current_coverage', 0)}% / {gap.get('expected_coverage', 0)}%")
            recs = gap.get('recommendations', [])
            if recs:
                report_lines.append(f"- **Acción:** {recs[0]}")
            report_lines.append("")
    else:
        report_lines.append("No hay brechas altas identificadas.\n")
    
    report_content = "\n".join(report_lines)
    
    # Guardar
    if output_file:
        filepath = Path(output_file)
    else:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        gaps_dir = REPORTS_DIR / "gaps"
        gaps_dir.mkdir(exist_ok=True)
        filepath = gaps_dir / f"gap_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filepath, 'w') as f:
        f.write(report_content)
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Reporte de brechas generado:[/green] {filepath}")
    else:
        print(f"\n✅ Reporte de brechas generado: {filepath}")
    
    return str(filepath)

def generate_metrics_report(output_file: Optional[str] = None) -> str:
    """Generar reporte de métricas."""
    metrics = calculate_metrics()
    
    report_lines = []
    report_lines.append("# 📈 Purple Team Metrics Report\n")
    report_lines.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("---\n")
    
    # KPIs Principales
    report_lines.append("## 🎯 KPIs Principales\n")
    report_lines.append("| Métrica | Valor | Objetivo | Estado |")
    report_lines.append("|---------|-------|----------|--------|")
    
    # Cobertura
    cov_status = "✅" if metrics.average_coverage >= 70 else "⚠️" if metrics.average_coverage >= 50 else "❌"
    report_lines.append(f"| Cobertura de Detección | {metrics.average_coverage:.1f}% | ≥70% | {cov_status} |")
    
    # Tasa de detección
    if metrics.total_techniques_tested > 0:
        detection_rate = (metrics.techniques_detected / metrics.total_techniques_tested) * 100
    else:
        detection_rate = 0
    det_status = "✅" if detection_rate >= 80 else "⚠️" if detection_rate >= 60 else "❌"
    report_lines.append(f"| Tasa de Detección | {detection_rate:.1f}% | ≥80% | {det_status} |")
    
    # Brechas críticas
    crit_status = "✅" if metrics.critical_gaps == 0 else "❌"
    report_lines.append(f"| Brechas Críticas | {metrics.critical_gaps} | 0 | {crit_status} |")
    
    report_lines.append("\n---\n")
    
    # Desglose de Técnicas
    report_lines.append("## 📊 Desglose de Técnicas\n")
    report_lines.append(f"- **Total Probadas:** {metrics.total_techniques_tested}")
    report_lines.append(f"- **Detectadas:** {metrics.techniques_detected}")
    report_lines.append(f"- **No Detectadas:** {metrics.techniques_not_detected}\n")
    
    # Gráfico ASCII
    if metrics.total_techniques_tested > 0:
        detected_pct = int((metrics.techniques_detected / metrics.total_techniques_tested) * 20)
        not_detected_pct = 20 - detected_pct
        report_lines.append("```")
        report_lines.append(f"Detectadas:     {'█' * detected_pct}{'░' * not_detected_pct} {metrics.techniques_detected}")
        report_lines.append(f"No Detectadas:  {'█' * not_detected_pct}{'░' * detected_pct} {metrics.techniques_not_detected}")
        report_lines.append("```\n")
    
    report_lines.append("---\n")
    
    # Distribución de Brechas
    report_lines.append("## ⚠️ Distribución de Brechas\n")
    report_lines.append(f"- 🔴 Críticas: {metrics.critical_gaps}")
    report_lines.append(f"- 🟠 Altas: {metrics.high_gaps}")
    report_lines.append(f"- 🟡 Medias: {metrics.medium_gaps}")
    report_lines.append(f"- 🔵 Bajas: {metrics.low_gaps}\n")
    
    total_gaps = metrics.critical_gaps + metrics.high_gaps + metrics.medium_gaps + metrics.low_gaps
    report_lines.append(f"**Total de Brechas:** {total_gaps}\n")
    
    report_lines.append("---\n")
    
    # Tendencias (placeholder)
    report_lines.append("## 📈 Tendencias\n")
    report_lines.append("*Nota: Las tendencias se calcularán con datos históricos.*\n")
    report_lines.append("| Período | Cobertura | Brechas | Tendencia |")
    report_lines.append("|---------|-----------|---------|-----------|")
    report_lines.append(f"| Actual | {metrics.average_coverage:.1f}% | {total_gaps} | - |")
    report_lines.append("| Anterior | - | - | - |")
    report_lines.append("| Hace 30 días | - | - | - |\n")
    
    report_content = "\n".join(report_lines)
    
    # Guardar
    if output_file:
        filepath = Path(output_file)
    else:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        metrics_dir = REPORTS_DIR / "metrics"
        metrics_dir.mkdir(exist_ok=True)
        filepath = metrics_dir / f"metrics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filepath, 'w') as f:
        f.write(report_content)
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Reporte de métricas generado:[/green] {filepath}")
    else:
        print(f"\n✅ Reporte de métricas generado: {filepath}")
    
    return str(filepath)

def generate_executive_summary(output_file: Optional[str] = None) -> str:
    """Generar resumen ejecutivo."""
    metrics = calculate_metrics()
    
    report_lines = []
    report_lines.append("# 🟣 Purple Team - Resumen Ejecutivo\n")
    report_lines.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("---\n")
    
    # Estado General
    if metrics.average_coverage >= 80 and metrics.critical_gaps == 0:
        status = "🟢 EXCELENTE"
        status_desc = "Los controles de seguridad están funcionando correctamente."
    elif metrics.average_coverage >= 60:
        status = "🟡 BUENO"
        status_desc = "Hay áreas de mejora identificadas pero el riesgo es manejable."
    elif metrics.average_coverage >= 40:
        status = "🟠 REGULAR"
        status_desc = "Se requiere atención inmediata en varias áreas."
    else:
        status = "🔴 CRÍTICO"
        status_desc = "Existen brechas significativas que requieren acción urgente."
    
    report_lines.append(f"## Estado General: {status}\n")
    report_lines.append(f"{status_desc}\n")
    report_lines.append("---\n")
    
    # Métricas Clave
    report_lines.append("## 📊 Métricas Clave\n")
    report_lines.append(f"| Indicador | Valor |")
    report_lines.append(f"|-----------|-------|")
    report_lines.append(f"| Cobertura de Detección | **{metrics.average_coverage:.1f}%** |")
    report_lines.append(f"| Técnicas Validadas | **{metrics.total_techniques_tested}** |")
    report_lines.append(f"| Brechas Críticas | **{metrics.critical_gaps}** |")
    report_lines.append(f"| Brechas Totales | **{metrics.critical_gaps + metrics.high_gaps + metrics.medium_gaps + metrics.low_gaps}** |\n")
    
    report_lines.append("---\n")
    
    # Hallazgos Principales
    report_lines.append("## 🔍 Hallazgos Principales\n")
    
    if metrics.critical_gaps > 0:
        report_lines.append(f"- ⚠️ **{metrics.critical_gaps} brechas críticas** requieren atención inmediata")
    
    if metrics.techniques_not_detected > 0:
        report_lines.append(f"- 🔴 **{metrics.techniques_not_detected} técnicas** no fueron detectadas")
    
    if metrics.average_coverage < 70:
        report_lines.append(f"- 📉 La cobertura promedio ({metrics.average_coverage:.1f}%) está por debajo del objetivo (70%)")
    
    if metrics.average_coverage >= 80:
        report_lines.append("- ✅ La cobertura de detección cumple con los objetivos")
    
    report_lines.append("\n---\n")
    
    # Recomendaciones
    report_lines.append("## 📋 Recomendaciones\n")
    report_lines.append("1. **Prioridad Alta:** Implementar detecciones para técnicas críticas sin cobertura")
    report_lines.append("2. **Prioridad Media:** Mejorar reglas existentes para reducir falsos positivos")
    report_lines.append("3. **Prioridad Normal:** Documentar y actualizar playbooks de respuesta")
    report_lines.append("4. **Continuo:** Programar ejercicios Purple Team mensuales\n")
    
    report_lines.append("---\n")
    
    # Próximo Ejercicio
    report_lines.append("## 📅 Próximo Ejercicio\n")
    next_date = datetime.now() + timedelta(days=30)
    report_lines.append(f"- **Fecha Sugerida:** {next_date.strftime('%Y-%m-%d')}")
    report_lines.append("- **Enfoque:** Validación de correcciones implementadas")
    report_lines.append("- **Técnicas a Probar:** Brechas críticas y altas identificadas\n")
    
    report_content = "\n".join(report_lines)
    
    # Guardar
    if output_file:
        filepath = Path(output_file)
    else:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        filepath = REPORTS_DIR / f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filepath, 'w') as f:
        f.write(report_content)
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Resumen ejecutivo generado:[/green] {filepath}")
    else:
        print(f"\n✅ Resumen ejecutivo generado: {filepath}")
    
    return str(filepath)

def generate_full_report(output_file: Optional[str] = None) -> str:
    """Generar reporte completo."""
    if RICH_AVAILABLE:
        console.print("\n[cyan]Generando reporte completo...[/cyan]")
    
    # Generar todos los reportes
    reports = []
    reports.append(generate_executive_summary())
    reports.append(generate_exercise_report())
    reports.append(generate_gap_report())
    reports.append(generate_metrics_report())
    
    if RICH_AVAILABLE:
        console.print(f"\n[green]✅ Reportes generados:[/green]")
        for report in reports:
            console.print(f"   • {report}")
    else:
        print("\n✅ Reportes generados:")
        for report in reports:
            print(f"   • {report}")
    
    return reports[0]

def display_summary():
    """Mostrar resumen en consola."""
    metrics = calculate_metrics()
    
    if RICH_AVAILABLE:
        console.print("\n[bold purple]" + "═" * 70 + "[/bold purple]")
        console.print("[bold purple]  📊 RESUMEN PURPLE TEAM[/bold purple]")
        console.print("[bold purple]" + "═" * 70 + "[/bold purple]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Métrica", style="white")
        table.add_column("Valor", justify="right")
        
        table.add_row("Técnicas Probadas", str(metrics.total_techniques_tested))
        table.add_row("Técnicas Detectadas", f"[green]{metrics.techniques_detected}[/green]")
        table.add_row("Técnicas No Detectadas", f"[red]{metrics.techniques_not_detected}[/red]")
        table.add_row("Cobertura Promedio", f"{metrics.average_coverage:.1f}%")
        table.add_row("Brechas Críticas", f"[red]{metrics.critical_gaps}[/red]")
        table.add_row("Brechas Altas", f"[orange1]{metrics.high_gaps}[/orange1]")
        table.add_row("Brechas Medias", f"[yellow]{metrics.medium_gaps}[/yellow]")
        table.add_row("Brechas Bajas", f"[blue]{metrics.low_gaps}[/blue]")
        
        console.print(table)
    else:
        print("\n" + "═" * 70)
        print("  📊 RESUMEN PURPLE TEAM")
        print("═" * 70)
        print(f"\n  Técnicas Probadas:      {metrics.total_techniques_tested}")
        print(f"  Técnicas Detectadas:    {metrics.techniques_detected}")
        print(f"  Técnicas No Detectadas: {metrics.techniques_not_detected}")
        print(f"  Cobertura Promedio:     {metrics.average_coverage:.1f}%")
        print(f"  Brechas Críticas:       {metrics.critical_gaps}")

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="📊 Purple Report - Generador de Reportes",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-e', '--exercise-report',
        action='store_true',
        help='Generar reporte de ejercicio'
    )
    parser.add_argument(
        '-g', '--gap-report',
        action='store_true',
        help='Generar reporte de brechas'
    )
    parser.add_argument(
        '-m', '--metrics-report',
        action='store_true',
        help='Generar reporte de métricas'
    )
    parser.add_argument(
        '-s', '--executive-summary',
        action='store_true',
        help='Generar resumen ejecutivo'
    )
    parser.add_argument(
        '-f', '--full-report',
        action='store_true',
        help='Generar reporte completo'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Mostrar resumen en consola'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo de salida'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.exercise_report:
        generate_exercise_report(args.output)
    elif args.gap_report:
        generate_gap_report(args.output)
    elif args.metrics_report:
        generate_metrics_report(args.output)
    elif args.executive_summary:
        generate_executive_summary(args.output)
    elif args.full_report:
        generate_full_report(args.output)
    elif args.summary:
        display_summary()
    else:
        display_summary()
        parser.print_help()

if __name__ == "__main__":
    main()
