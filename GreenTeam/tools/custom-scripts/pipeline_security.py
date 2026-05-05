#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   🟢 GREEN TEAM - Security Pipeline Orchestrator                            ║
║   Pipeline completo de seguridad DevSecOps                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import subprocess
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WARNING = "warning"

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class StageResult:
    name: str
    status: StageStatus
    duration: float = 0.0
    findings: Dict[str, int] = field(default_factory=dict)
    report_path: Optional[str] = None
    error: Optional[str] = None

@dataclass
class PipelineResult:
    start_time: datetime
    end_time: Optional[datetime] = None
    stages: List[StageResult] = field(default_factory=list)
    overall_status: StageStatus = StageStatus.PENDING

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    PURPLE = '\033[0;35m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"{Colors.GREEN}")
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                           ║")
    print("║   ██████╗ ██████╗ ███████╗███████╗███╗   ██╗    ████████╗███████╗ █████╗  ║")
    print("║  ██╔════╝ ██╔══██╗██╔════╝██╔════╝████╗  ██║    ╚══██╔══╝██╔════╝██╔══██╗ ║")
    print("║  ██║  ███╗██████╔╝█████╗  █████╗  ██╔██╗ ██║       ██║   █████╗  ███████║ ║")
    print("║  ██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║       ██║   ██╔══╝  ██╔══██║ ║")
    print("║  ╚██████╔╝██║  ██║███████╗███████╗██║ ╚████║       ██║   ███████╗██║  ██║ ║")
    print("║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝       ╚═╝   ╚══════╝╚═╝  ╚═╝ ║")
    print("║                                                                           ║")
    print("║                    🔄 Security Pipeline Orchestrator                      ║")
    print("║                                                                           ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.NC}")

def log_stage(stage: str, status: str = ""):
    icon = {
        "start": "🔄",
        "pass": "✅",
        "fail": "❌",
        "warn": "⚠️",
        "skip": "⏭️"
    }.get(status, "📋")
    print(f"\n{Colors.CYAN}{'═' * 70}{Colors.NC}")
    print(f"{icon} {Colors.BOLD}{stage}{Colors.NC}")
    print(f"{Colors.CYAN}{'═' * 70}{Colors.NC}")

def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def log_success(msg: str):
    print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")

def log_warning(msg: str):
    print(f"{Colors.YELLOW}[!]{Colors.NC} {msg}")

def log_error(msg: str):
    print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

def check_tool(tool: str) -> bool:
    """Verificar si una herramienta está instalada."""
    try:
        subprocess.run([tool, "--version"], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False

def run_command(cmd: List[str], cwd: Optional[str] = None, timeout: int = 300) -> tuple:
    """Ejecutar comando y retornar stdout, stderr, return_code."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout expired", -1
    except Exception as e:
        return "", str(e), -1

class SecurityPipeline:
    def __init__(self, target: Path, output_dir: Path):
        self.target = target
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = output_dir / "pipeline" / self.timestamp
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.result = PipelineResult(start_time=datetime.now())
        
        # Security gates
        self.gates = {
            "critical": 0,
            "high": 5,
            "secrets": 0
        }
    
    def run_stage(self, name: str, func, *args, **kwargs) -> StageResult:
        """Ejecutar una etapa del pipeline."""
        log_stage(name, "start")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            result.duration = duration
            
            if result.status == StageStatus.PASSED:
                log_stage(name, "pass")
            elif result.status == StageStatus.WARNING:
                log_stage(name, "warn")
            elif result.status == StageStatus.FAILED:
                log_stage(name, "fail")
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            log_error(f"Error en {name}: {str(e)}")
            return StageResult(
                name=name,
                status=StageStatus.FAILED,
                duration=duration,
                error=str(e)
            )
    
    def stage_secrets(self) -> StageResult:
        """Etapa: Detección de secrets."""
        result = StageResult(name="Secret Detection", status=StageStatus.PENDING)
        findings = {"gitleaks": 0, "trufflehog": 0, "detect_secrets": 0}
        
        # Gitleaks
        if check_tool("gitleaks"):
            log_info("Ejecutando Gitleaks...")
            report_path = self.report_dir / "gitleaks.json"
            stdout, stderr, rc = run_command([
                "gitleaks", "detect",
                "--source", str(self.target),
                "--report-format", "json",
                "--report-path", str(report_path),
                "--no-git"
            ])
            
            if report_path.exists():
                try:
                    with open(report_path) as f:
                        data = json.load(f)
                        findings["gitleaks"] = len(data) if isinstance(data, list) else 0
                except:
                    pass
            log_success(f"Gitleaks: {findings['gitleaks']} secrets encontrados")
        
        # TruffleHog
        if check_tool("trufflehog"):
            log_info("Ejecutando TruffleHog...")
            report_path = self.report_dir / "trufflehog.json"
            stdout, stderr, rc = run_command([
                "trufflehog", "filesystem",
                str(self.target),
                "--json"
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                findings["trufflehog"] = len(stdout.strip().split("\n")) if stdout.strip() else 0
            log_success(f"TruffleHog: {findings['trufflehog']} credenciales encontradas")
        
        # detect-secrets
        if check_tool("detect-secrets"):
            log_info("Ejecutando detect-secrets...")
            report_path = self.report_dir / "detect-secrets.json"
            stdout, stderr, rc = run_command([
                "detect-secrets", "scan",
                str(self.target)
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                try:
                    data = json.loads(stdout)
                    findings["detect_secrets"] = sum(len(v) for v in data.get("results", {}).values())
                except:
                    pass
            log_success(f"detect-secrets: {findings['detect_secrets']} posibles secrets")
        
        total = sum(findings.values())
        result.findings = findings
        result.report_path = str(self.report_dir)
        
        if total > 0:
            result.status = StageStatus.FAILED
            log_error(f"Total secrets encontrados: {total}")
        else:
            result.status = StageStatus.PASSED
            log_success("No se encontraron secrets expuestos")
        
        return result
    
    def stage_sast(self) -> StageResult:
        """Etapa: SAST - Static Application Security Testing."""
        result = StageResult(name="SAST Scan", status=StageStatus.PENDING)
        findings = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        # Semgrep
        if check_tool("semgrep"):
            log_info("Ejecutando Semgrep...")
            report_path = self.report_dir / "semgrep.json"
            stdout, stderr, rc = run_command([
                "semgrep", "scan",
                "--config", "auto",
                str(self.target),
                "--json"
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                try:
                    data = json.loads(stdout)
                    for r in data.get("results", []):
                        severity = r.get("extra", {}).get("severity", "INFO").upper()
                        if severity == "ERROR":
                            findings["critical"] += 1
                        elif severity == "WARNING":
                            findings["high"] += 1
                        elif severity == "INFO":
                            findings["medium"] += 1
                except:
                    pass
            log_success(f"Semgrep completado")
        
        # Bandit (Python)
        if check_tool("bandit"):
            log_info("Ejecutando Bandit...")
            report_path = self.report_dir / "bandit.json"
            stdout, stderr, rc = run_command([
                "bandit", "-r", str(self.target),
                "-f", "json"
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                try:
                    data = json.loads(stdout)
                    for r in data.get("results", []):
                        severity = r.get("issue_severity", "LOW").upper()
                        if severity == "HIGH":
                            findings["high"] += 1
                        elif severity == "MEDIUM":
                            findings["medium"] += 1
                        else:
                            findings["low"] += 1
                except:
                    pass
            log_success(f"Bandit completado")
        
        result.findings = findings
        result.report_path = str(self.report_dir)
        
        if findings["critical"] > 0:
            result.status = StageStatus.FAILED
        elif findings["high"] > self.gates["high"]:
            result.status = StageStatus.WARNING
        else:
            result.status = StageStatus.PASSED
        
        log_info(f"SAST: Critical={findings['critical']}, High={findings['high']}, Medium={findings['medium']}, Low={findings['low']}")
        
        return result
    
    def stage_sca(self) -> StageResult:
        """Etapa: SCA - Software Composition Analysis."""
        result = StageResult(name="SCA Scan", status=StageStatus.PENDING)
        findings = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        # Safety (Python)
        if check_tool("safety") and (self.target / "requirements.txt").exists():
            log_info("Ejecutando Safety...")
            report_path = self.report_dir / "safety.json"
            stdout, stderr, rc = run_command([
                "safety", "check",
                "-r", str(self.target / "requirements.txt"),
                "--json"
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
            log_success("Safety completado")
        
        # npm audit (Node.js)
        if check_tool("npm") and (self.target / "package.json").exists():
            log_info("Ejecutando npm audit...")
            report_path = self.report_dir / "npm-audit.json"
            stdout, stderr, rc = run_command(
                ["npm", "audit", "--json"],
                cwd=str(self.target)
            )
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                try:
                    data = json.loads(stdout)
                    vulns = data.get("vulnerabilities", {})
                    for name, info in vulns.items():
                        severity = info.get("severity", "low")
                        if severity == "critical":
                            findings["critical"] += 1
                        elif severity == "high":
                            findings["high"] += 1
                        elif severity in ["moderate", "medium"]:
                            findings["medium"] += 1
                        else:
                            findings["low"] += 1
                except:
                    pass
            log_success("npm audit completado")
        
        # Snyk
        if check_tool("snyk"):
            log_info("Ejecutando Snyk...")
            report_path = self.report_dir / "snyk.json"
            stdout, stderr, rc = run_command([
                "snyk", "test",
                "--json",
                str(self.target)
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
            log_success("Snyk completado")
        
        result.findings = findings
        result.report_path = str(self.report_dir)
        
        if findings["critical"] > 0:
            result.status = StageStatus.FAILED
        elif findings["high"] > self.gates["high"]:
            result.status = StageStatus.WARNING
        else:
            result.status = StageStatus.PASSED
        
        log_info(f"SCA: Critical={findings['critical']}, High={findings['high']}, Medium={findings['medium']}, Low={findings['low']}")
        
        return result
    
    def stage_iac(self) -> StageResult:
        """Etapa: IaC Security Scan."""
        result = StageResult(name="IaC Security", status=StageStatus.PENDING)
        findings = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        # Checkov
        if check_tool("checkov"):
            log_info("Ejecutando Checkov...")
            report_path = self.report_dir / "checkov.json"
            stdout, stderr, rc = run_command([
                "checkov",
                "-d", str(self.target),
                "-o", "json"
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                try:
                    data = json.loads(stdout)
                    if isinstance(data, list):
                        for check in data:
                            failed = check.get("summary", {}).get("failed", 0)
                            findings["high"] += failed
                except:
                    pass
            log_success("Checkov completado")
        
        # tfsec
        if check_tool("tfsec"):
            tf_files = list(self.target.glob("**/*.tf"))
            if tf_files:
                log_info("Ejecutando tfsec...")
                report_path = self.report_dir / "tfsec.json"
                stdout, stderr, rc = run_command([
                    "tfsec", str(self.target),
                    "--format", "json"
                ])
                
                if stdout:
                    with open(report_path, "w") as f:
                        f.write(stdout)
                log_success("tfsec completado")
        
        result.findings = findings
        result.report_path = str(self.report_dir)
        
        if findings["critical"] > 0:
            result.status = StageStatus.FAILED
        elif findings["high"] > 0:
            result.status = StageStatus.WARNING
        else:
            result.status = StageStatus.PASSED
        
        return result
    
    def stage_container(self, image: Optional[str] = None) -> StageResult:
        """Etapa: Container Security Scan."""
        result = StageResult(name="Container Security", status=StageStatus.PENDING)
        findings = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        # Hadolint para Dockerfiles
        dockerfiles = list(self.target.glob("**/Dockerfile*"))
        if check_tool("hadolint") and dockerfiles:
            log_info("Ejecutando Hadolint...")
            for dockerfile in dockerfiles:
                report_path = self.report_dir / f"hadolint-{dockerfile.name}.json"
                stdout, stderr, rc = run_command([
                    "hadolint", str(dockerfile),
                    "--format", "json"
                ])
                
                if stdout:
                    with open(report_path, "w") as f:
                        f.write(stdout)
            log_success("Hadolint completado")
        
        # Trivy para imagen
        if image and check_tool("trivy"):
            log_info(f"Ejecutando Trivy en imagen: {image}")
            report_path = self.report_dir / "trivy-image.json"
            stdout, stderr, rc = run_command([
                "trivy", "image",
                image,
                "--format", "json"
            ])
            
            if stdout:
                with open(report_path, "w") as f:
                    f.write(stdout)
                try:
                    data = json.loads(stdout)
                    for r in data.get("Results", []):
                        for v in r.get("Vulnerabilities", []):
                            severity = v.get("Severity", "LOW").upper()
                            if severity == "CRITICAL":
                                findings["critical"] += 1
                            elif severity == "HIGH":
                                findings["high"] += 1
                            elif severity == "MEDIUM":
                                findings["medium"] += 1
                            else:
                                findings["low"] += 1
                except:
                    pass
            log_success("Trivy completado")
        
        result.findings = findings
        result.report_path = str(self.report_dir)
        
        if findings["critical"] > 0:
            result.status = StageStatus.FAILED
        elif findings["high"] > self.gates["high"]:
            result.status = StageStatus.WARNING
        else:
            result.status = StageStatus.PASSED
        
        return result
    
    def generate_report(self):
        """Generar reporte final del pipeline."""
        report_path = self.report_dir / "pipeline_report.md"
        
        total_findings = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for stage in self.result.stages:
            for severity, count in stage.findings.items():
                if severity in total_findings:
                    total_findings[severity] += count
        
        duration = (self.result.end_time - self.result.start_time).total_seconds()
        
        with open(report_path, "w") as f:
            f.write("# 🔄 Security Pipeline Report\n\n")
            f.write(f"**Fecha:** {self.result.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Duración:** {duration:.2f} segundos\n")
            f.write(f"**Target:** {self.target}\n")
            f.write(f"**Estado:** {self.result.overall_status.value.upper()}\n\n")
            
            f.write("## 📊 Resumen de Vulnerabilidades\n\n")
            f.write("| Severidad | Cantidad |\n")
            f.write("|-----------|----------|\n")
            f.write(f"| 🔴 Crítica | {total_findings['critical']} |\n")
            f.write(f"| 🟠 Alta | {total_findings['high']} |\n")
            f.write(f"| 🟡 Media | {total_findings['medium']} |\n")
            f.write(f"| 🔵 Baja | {total_findings['low']} |\n\n")
            
            f.write("## 📋 Etapas del Pipeline\n\n")
            f.write("| Etapa | Estado | Duración | Findings |\n")
            f.write("|-------|--------|----------|----------|\n")
            
            for stage in self.result.stages:
                status_icon = {
                    StageStatus.PASSED: "✅",
                    StageStatus.FAILED: "❌",
                    StageStatus.WARNING: "⚠️",
                    StageStatus.SKIPPED: "⏭️"
                }.get(stage.status, "❓")
                
                findings_str = ", ".join(f"{k}:{v}" for k, v in stage.findings.items() if v > 0) or "0"
                f.write(f"| {stage.name} | {status_icon} {stage.status.value} | {stage.duration:.2f}s | {findings_str} |\n")
            
            f.write("\n## 🚨 Security Gate\n\n")
            if self.result.overall_status == StageStatus.PASSED:
                f.write("**✅ PASSED** - El pipeline cumple con los criterios de seguridad.\n")
            elif self.result.overall_status == StageStatus.WARNING:
                f.write("**⚠️ WARNING** - Se encontraron issues que requieren atención.\n")
            else:
                f.write("**❌ FAILED** - El pipeline no cumple con los criterios de seguridad.\n")
            
            f.write("\n### Criterios de Gate\n\n")
            f.write(f"- Vulnerabilidades Críticas: máximo {self.gates['critical']}\n")
            f.write(f"- Vulnerabilidades Altas: máximo {self.gates['high']}\n")
            f.write(f"- Secrets Expuestos: máximo {self.gates['secrets']}\n")
        
        # JSON report
        json_report = {
            "timestamp": self.result.start_time.isoformat(),
            "duration": duration,
            "target": str(self.target),
            "status": self.result.overall_status.value,
            "total_findings": total_findings,
            "stages": [
                {
                    "name": s.name,
                    "status": s.status.value,
                    "duration": s.duration,
                    "findings": s.findings,
                    "error": s.error
                }
                for s in self.result.stages
            ]
        }
        
        with open(self.report_dir / "pipeline_report.json", "w") as f:
            json.dump(json_report, f, indent=2)
        
        return report_path
    
    def print_summary(self):
        """Imprimir resumen del pipeline."""
        duration = (self.result.end_time - self.result.start_time).total_seconds()
        
        print(f"\n{Colors.CYAN}{'═' * 70}{Colors.NC}")
        print(f"{Colors.BOLD}📊 RESUMEN DEL PIPELINE{Colors.NC}")
        print(f"{Colors.CYAN}{'═' * 70}{Colors.NC}\n")
        
        # Tabla de etapas
        print(f"{'Etapa':<25} {'Estado':<15} {'Duración':<12} {'Findings'}")
        print(f"{'-' * 70}")
        
        for stage in self.result.stages:
            status_color = {
                StageStatus.PASSED: Colors.GREEN,
                StageStatus.FAILED: Colors.RED,
                StageStatus.WARNING: Colors.YELLOW,
                StageStatus.SKIPPED: Colors.BLUE
            }.get(stage.status, Colors.NC)
            
            status_icon = {
                StageStatus.PASSED: "✅",
                StageStatus.FAILED: "❌",
                StageStatus.WARNING: "⚠️",
                StageStatus.SKIPPED: "⏭️"
            }.get(stage.status, "❓")
            
            findings_str = ", ".join(f"{k}:{v}" for k, v in stage.findings.items() if v > 0) or "-"
            
            print(f"{stage.name:<25} {status_color}{status_icon} {stage.status.value:<12}{Colors.NC} {stage.duration:>6.2f}s     {findings_str}")
        
        print(f"\n{Colors.CYAN}{'─' * 70}{Colors.NC}")
        print(f"Duración total: {duration:.2f} segundos")
        print(f"{Colors.CYAN}{'─' * 70}{Colors.NC}")
        
        # Estado final
        if self.result.overall_status == StageStatus.PASSED:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SECURITY GATE: PASSED{Colors.NC}")
        elif self.result.overall_status == StageStatus.WARNING:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ SECURITY GATE: WARNING{Colors.NC}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ SECURITY GATE: FAILED{Colors.NC}")
        
        print(f"\nReportes: {Colors.CYAN}{self.report_dir}{Colors.NC}\n")
    
    def run(self, stages: Optional[List[str]] = None, image: Optional[str] = None):
        """Ejecutar el pipeline completo."""
        all_stages = ["secrets", "sast", "sca", "iac", "container"]
        stages_to_run = stages if stages else all_stages
        
        log_info(f"Iniciando pipeline de seguridad...")
        log_info(f"Target: {self.target}")
        log_info(f"Etapas: {', '.join(stages_to_run)}")
        
        # Ejecutar etapas
        if "secrets" in stages_to_run:
            result = self.run_stage("Secret Detection", self.stage_secrets)
            self.result.stages.append(result)
        
        if "sast" in stages_to_run:
            result = self.run_stage("SAST Scan", self.stage_sast)
            self.result.stages.append(result)
        
        if "sca" in stages_to_run:
            result = self.run_stage("SCA Scan", self.stage_sca)
            self.result.stages.append(result)
        
        if "iac" in stages_to_run:
            result = self.run_stage("IaC Security", self.stage_iac)
            self.result.stages.append(result)
        
        if "container" in stages_to_run:
            result = self.run_stage("Container Security", self.stage_container, image)
            self.result.stages.append(result)
        
        # Determinar estado general
        self.result.end_time = datetime.now()
        
        has_failed = any(s.status == StageStatus.FAILED for s in self.result.stages)
        has_warning = any(s.status == StageStatus.WARNING for s in self.result.stages)
        
        if has_failed:
            self.result.overall_status = StageStatus.FAILED
        elif has_warning:
            self.result.overall_status = StageStatus.WARNING
        else:
            self.result.overall_status = StageStatus.PASSED
        
        # Generar reportes
        self.generate_report()
        self.print_summary()
        
        return self.result.overall_status != StageStatus.FAILED

def main():
    parser = argparse.ArgumentParser(
        description="GREEN TEAM Security Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                          # Pipeline completo en directorio actual
  %(prog)s /path/to/project         # Pipeline completo en directorio específico
  %(prog)s --stages secrets sast    # Solo etapas específicas
  %(prog)s --image nginx:latest     # Incluir escaneo de imagen Docker
        """
    )
    
    parser.add_argument("target", nargs="?", default=".", help="Directorio a escanear")
    parser.add_argument("-o", "--output", default=None, help="Directorio de salida para reportes")
    parser.add_argument("-s", "--stages", nargs="+", 
                       choices=["secrets", "sast", "sca", "iac", "container"],
                       help="Etapas específicas a ejecutar")
    parser.add_argument("-i", "--image", default=None, help="Imagen Docker a escanear")
    parser.add_argument("--gate-critical", type=int, default=0, help="Máximo de vulnerabilidades críticas")
    parser.add_argument("--gate-high", type=int, default=5, help="Máximo de vulnerabilidades altas")
    parser.add_argument("-q", "--quiet", action="store_true", help="Modo silencioso")
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    target = Path(args.target).resolve()
    output_dir = Path(args.output) if args.output else target / "scans"
    
    if not target.exists():
        log_error(f"El directorio no existe: {target}")
        sys.exit(1)
    
    pipeline = SecurityPipeline(target, output_dir)
    pipeline.gates["critical"] = args.gate_critical
    pipeline.gates["high"] = args.gate_high
    
    success = pipeline.run(stages=args.stages, image=args.image)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
